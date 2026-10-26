import os
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QColor, QKeySequence, QShortcut, QAction, QBrush, QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QColorDialog, QMenu, QMessageBox, QApplication,
    QPushButton, QGraphicsOpacityEffect, QLabel
)

from src.config import load_settings, save_settings
from src.image_loader import ImageManager
from src.control_panel import ControlPanel
from src.settings_dialog import SettingsDialog


class PhotoViewerWindow(QMainWindow):
    def __init__(self, image_dir="images", start_file=None):
        super().__init__()
        
        # Load cấu hình đã lưu
        self.settings = load_settings()
        
        # Lấy thư mục từ cấu hình (nếu chưa có dùng image_dir)
        self.current_folder = self.settings.get("image_folder", image_dir)
        self.image_manager = ImageManager(image_dir=self.current_folder)
        
        # Nạp danh sách và khóa thẳng index vào file được chọn
        self.image_manager.load_images(start_file=start_file)
        
        self.interval_ms = self.settings.get("interval_ms", 3000)
        self.bg_color = QColor(self.settings.get("bg_color", "#000000"))
        
        # Bật sẵn chế độ tự động trình chiếu khi mở từ bên ngoài
        self.is_playing = True

        self.init_ui()
        # --- KHÔI PHỤC VỊ TRÍ VÀ TRẠNG THÁI CỬA SỔ CŨ ---
        saved_geometry = self.settings.get("window_geometry")
        if saved_geometry and len(saved_geometry) == 4:
            # Đặt tọa độ kích thước khung bình thường trước
            self.setGeometry(saved_geometry[0], saved_geometry[1], saved_geometry[2], saved_geometry[3])
            
        # Sau đó mới set trạng thái phóng to (nếu có)
        if self.settings.get("is_maximized", False):
            self.showMaximized()
        elif self.settings.get("is_fullscreen", False):
            self.showFullScreen()
        # ---------------------------------------------

        self.show_image()  # Hiển thị trực tiếp ảnh đúng vị trí

        # Timer trình chiếu tự động
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image_auto)
        if self.image_manager.image_paths:
            self.timer.start(self.interval_ms)

        # Timer phân biệt Click đơn (Pause/Play) và Click đúp (Fullscreen)
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.toggle_play_pause)

    def init_ui(self):
        self.setWindowTitle("Windows Photo Slideshow")
        self.resize(1050, 720)
        if os.path.exists("app_icon.ico"):
            self.setWindowIcon(QIcon("app_icon.ico"))
        elif os.path.exists("app_icon.png"):
            self.setWindowIcon(QIcon("app_icon.png"))

        # Central Widget & Layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Graphics Scene & View
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("border: none; background-color: transparent;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.installEventFilter(self)
        self.view.viewport().installEventFilter(self)
        self.main_layout.addWidget(self.view)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # Hiệu ứng Fade In / Fade Out khi đổi ảnh
        self.opacity_effect = QGraphicsOpacityEffect(self.view)
        self.view.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(350)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Style chung rõ nét
        style_overlay_btn = """
            QPushButton {
                background-color: rgba(28, 28, 28, 230);
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 80);
            }
            QPushButton:hover {
                background-color: rgba(0, 173, 181, 230);
                border-color: rgba(255, 255, 255, 150);
            }
        """

        # 1. Nút mũi tên Trái & Phải
        self.btn_side_prev = QPushButton("◄", self)
        self.btn_side_next = QPushButton("►", self)
        self.btn_side_prev.setStyleSheet(style_overlay_btn)
        self.btn_side_next.setStyleSheet(style_overlay_btn)
        self.btn_side_prev.clicked.connect(self.prev_image_manual)
        self.btn_side_next.clicked.connect(self.next_image_manual)

        # 2. Nút Cài đặt (⚙), Yêu thích (❤️) & Option (⋮) ở góc trên bên phải
        self.btn_top_settings = QPushButton("⚙", self)
        self.btn_top_settings.setStyleSheet(style_overlay_btn)
        self.btn_top_settings.clicked.connect(self.open_settings)

        self.btn_top_favorites = QPushButton("❤️", self)
        self.btn_top_favorites.setStyleSheet(style_overlay_btn)
        self.btn_top_favorites.clicked.connect(self.toggle_current_image_favorite)

        self.btn_top_option = QPushButton("⋮", self)
        self.btn_top_option.setStyleSheet(style_overlay_btn)
        self.btn_top_option.clicked.connect(self.show_options_menu)

        # 3. Thẻ hiển thị thông tin góc trái
        self.lbl_top_info = QLabel("0 / 0", self)
        self.lbl_top_info.setStyleSheet("""
            QLabel {
                background-color: rgba(28, 28, 28, 230);
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 600;
                padding: 6px 14px;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 80);
            }
        """)

        # 4. Nút hiện lại thanh công cụ khi bị ẩn
        self.btn_show_panel = QPushButton("👁️ Hiện thanh công cụ", self)
        self.btn_show_panel.setStyleSheet("""
            QPushButton {
                background-color: rgba(28, 28, 28, 230);
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
                border: 1px solid rgba(255, 255, 255, 80);
                font-weight: 600;
            }
            QPushButton:hover { background-color: rgba(0, 173, 181, 230); }
        """)
        self.btn_show_panel.hide()
        self.btn_show_panel.clicked.connect(self.toggle_control_panel)

        # 5. Thanh công cụ bên dưới
        self.control_panel = ControlPanel(self)
        self.control_panel.btn_play_pause.clicked.connect(self.toggle_play_pause)
        self.control_panel.btn_random.toggled.connect(self.toggle_random)
        self.control_panel.btn_color.clicked.connect(self.change_bg_color)
        self.control_panel.btn_hide.clicked.connect(self.toggle_control_panel)

        self.control_panel.set_interval_value(self.interval_ms // 1000)
        self.control_panel.interval_changed.connect(self.on_interval_changed)

        # Phím tắt
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self.prev_image_manual)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self.next_image_manual)
        QShortcut(QKeySequence(Qt.Key.Key_Space), self, self.toggle_play_pause)
        QShortcut(QKeySequence(Qt.Key.Key_F11), self, self.toggle_fullscreen)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self.exit_fullscreen)
        QShortcut(QKeySequence(Qt.Key.Key_H), self, self.toggle_control_panel)

        self.update_background()

    def eventFilter(self, watched, event):
        """Bắt mọi sự kiện chuột trực tiếp trên QGraphicsView / Viewport"""
        if watched in (self.view, self.view.viewport()):
            if event.type() == event.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.click_timer.start(220)
            elif event.type() == event.Type.MouseButtonDblClick:
                if event.button() == Qt.MouseButton.LeftButton:
                    if self.click_timer.isActive():
                        self.click_timer.stop()
                    self.toggle_fullscreen()
                    return True
        return super().eventFilter(watched, event)

    def reload_and_show(self):
        count = self.image_manager.load_images()
        if count > 0:
            self.show_image()
        else:
            self.lbl_top_info.setText(self.image_manager.get_info_text())

    def show_image(self):
        path = self.image_manager.get_current_path()
        if not path:
            return

        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.fade_anim.stop()
            self.fade_anim.setStartValue(0.3)
            self.fade_anim.setEndValue(1.0)
            
            self.pixmap_item.setPixmap(pixmap)
            self.scene.setSceneRect(self.pixmap_item.boundingRect())
            self.fit_image_in_view()
            self.lbl_top_info.setText(self.image_manager.get_info_text())
            self.lbl_top_info.adjustSize()
            
            self.fade_anim.start()
            
            # Cập nhật trạng thái active/inactive của nút ❤️ cho ảnh mới
            self.update_favorite_button_state()

    def fit_image_in_view(self):
        if not self.pixmap_item.pixmap().isNull():
            self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def next_image_manual(self):
        self.image_manager.next_index()
        self.show_image()
        if self.is_playing:
            self.timer.start(self.interval_ms)

    def prev_image_manual(self):
        self.image_manager.prev_index()
        self.show_image()
        if self.is_playing:
            self.timer.start(self.interval_ms)

    def next_image_auto(self):
        if self.is_playing:
            self.image_manager.next_index()
            self.show_image()

    def toggle_play_pause(self):
        self.is_playing = not self.is_playing
        self.control_panel.set_play_state(self.is_playing)
        if self.is_playing:
            self.timer.start(self.interval_ms)
        else:
            self.timer.stop()

    def toggle_random(self, checked):
        self.image_manager.is_random = checked
        self.lbl_top_info.setText(self.image_manager.get_info_text())
        self.lbl_top_info.adjustSize()

    def on_interval_changed(self, seconds):
        self.interval_ms = seconds * 1000
        if self.is_playing:
            self.timer.start(self.interval_ms)
        
        self.settings["interval_ms"] = self.interval_ms
        save_settings(self.settings)

    def change_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self, "Chọn màu nền trình chiếu")
        if color.isValid():
            self.bg_color = color
            self.update_background()
            self.settings["bg_color"] = color.name()
            save_settings(self.settings)

    def update_background(self):
        brush = QBrush(self.bg_color)
        self.scene.setBackgroundBrush(brush)
        self.view.setBackgroundBrush(brush)
        self.view.viewport().setStyleSheet(f"background-color: {self.bg_color.name()};")

    def toggle_control_panel(self):
        if self.control_panel.isVisible():
            self.control_panel.hide()
            self.btn_show_panel.show()
        else:
            self.control_panel.show()
            self.btn_show_panel.hide()

    def open_settings(self):
        was_playing = self.is_playing
        if was_playing:
            self.timer.stop()

        dialog = SettingsDialog(self)
        if dialog.exec():
            self.settings = load_settings()
            new_folder = self.settings.get("image_folder", self.current_folder)
            if new_folder != self.current_folder:
                self.current_folder = new_folder
                self.image_manager.image_dir = new_folder
                self.reload_and_show()

        if was_playing and self.image_manager.image_paths:
            self.timer.start(self.interval_ms)

    def open_favorites_window(self):
        """Mở cửa sổ quản lý ảnh yêu thích"""
        was_playing = self.is_playing
        if was_playing:
            self.timer.stop()

        from src.favorites_window import FavoritesWindow
        fav_win = FavoritesWindow(self)
        fav_win.exec()

        if was_playing and self.image_manager.image_paths:
            self.timer.start(self.interval_ms)

    def show_options_menu(self):
        path = self.image_manager.get_current_path()
        if not path:
            return

        was_playing = self.is_playing
        if was_playing:
            self.timer.stop()

        menu = QMenu(self)

        favorites = self.settings.get("favorites", [])
        is_fav = path in favorites
        fav_label = "❤️ Bỏ Yêu Thích" if is_fav else "🤍 Thêm Vào Yêu Thích"

        act_fav = QAction(fav_label, self)
        act_fav.triggered.connect(lambda: self.toggle_favorite(path))

        act_copy_file = QAction("📋 Copy Đường Dẫn Tệp Ảnh", self)
        act_copy_file.triggered.connect(lambda: QApplication.clipboard().setText(path))

        act_open_folder = QAction("📁 Mở Trong Thư Mục (Explorer)", self)
        act_open_folder.triggered.connect(self.open_file_in_explorer)

        act_delete = QAction("🗑️ Xóa Ảnh (Vào Thùng Rác)", self)
        act_delete.triggered.connect(self.delete_current_image)

        menu.addAction(act_fav)
        menu.addSeparator()
        menu.addAction(act_copy_file)
        menu.addAction(act_open_folder)
        menu.addSeparator()
        menu.addAction(act_delete)

        menu.exec(self.btn_top_option.mapToGlobal(QPoint(0, self.btn_top_option.height() + 5)))

        if was_playing and self.image_manager.image_paths:
            self.timer.start(self.interval_ms)

    def toggle_favorite(self, path):
        favorites = self.settings.get("favorites", [])
        if path in favorites:
            favorites.remove(path)
        else:
            favorites.append(path)
        
        self.settings["favorites"] = favorites
        save_settings(self.settings)

    def open_file_in_explorer(self):
        path = self.image_manager.get_current_path()
        if path:
            norm_path = os.path.normpath(path)
            os.system(f'explorer /select,"{norm_path}"')

    def delete_current_image(self):
        path = self.image_manager.get_current_path()
        if not path:
            return

        reply = QMessageBox.question(
            self, 'Xác nhận xóa',
            f"Bạn có chắc muốn chuyển file này vào thùng rác?\n{os.path.basename(path)}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, result = self.image_manager.delete_current_image()
            if success:
                if self.image_manager.image_paths:
                    self.show_image()
                else:
                    self.scene.clear()
                    self.lbl_top_info.setText(self.image_manager.get_info_text())

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def exit_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_image_in_view()
        
        btn_size = 38

        # 1. Thẻ thông tin phía trên bên trái
        self.lbl_top_info.move(20, 20)

        # 2. Vị trí các nút Option, Cài Đặt và Yêu Thích ở góc trên bên phải
        self.btn_top_option.setGeometry(self.width() - btn_size - 20, 20, btn_size, btn_size)
        self.btn_top_settings.setGeometry(self.width() - (btn_size * 2) - 30, 20, btn_size, btn_size)
        self.btn_top_favorites.setGeometry(self.width() - (btn_size * 3) - 40, 20, btn_size, btn_size)

        # 3. Vị trí nút mũi tên Trái & Phải 2 bên
        self.btn_side_prev.setGeometry(20, (self.height() - btn_size) // 2, btn_size, btn_size)
        self.btn_side_next.setGeometry(self.width() - btn_size - 20, (self.height() - btn_size) // 2, btn_size, btn_size)

        # 4. Vị trí nút hiện lại công cụ khi bị ẩn
        self.btn_show_panel.setGeometry((self.width() - 170) // 2, self.height() - 55, 170, 38)

        # 5. Thanh công cụ ở góc dưới màn hình
        panel_width = 540
        panel_height = 48
        self.control_panel.setGeometry(
            (self.width() - panel_width) // 2,
            self.height() - panel_height - 25,
            panel_width,
            panel_height
        )

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.view.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            child = self.childAt(event.pos())
            if child == self.view or child == self.central_widget or child == self.view.viewport():
                self.click_timer.start(220)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.click_timer.isActive():
                self.click_timer.stop()
            self.toggle_fullscreen()
        super().mouseDoubleClickEvent(event)

    def update_favorite_button_state(self):
        """Cập nhật giao diện nút ❤️: Trái tim đỏ (Active) hoặc Trái tim trắng (Inactive)"""
        path = self.image_manager.get_current_path()
        if not path:
            return

        favorites = self.settings.get("favorites", [])
        is_fav = path in favorites

        if is_fav:
            # Active: Trái tim đỏ
            self.btn_top_favorites.setText("❤️")
            self.btn_top_favorites.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 28, 28, 230);
                    color: red;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 18px;
                    border: 2px solid rgba(255, 0, 0, 180);
                }
                QPushButton:hover {
                    background-color: rgba(50, 50, 50, 230);
                }
            """)
        else:
            # Inactive: Trái tim trắng (hoặc icon viền trắng)
            self.btn_top_favorites.setText("🤍")
            self.btn_top_favorites.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 28, 28, 230);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 18px;
                    border: 1px solid rgba(255, 255, 255, 80);
                }
                QPushButton:hover {
                    background-color: rgba(0, 173, 181, 230);
                    border-color: rgba(255, 255, 255, 150);
                }
            """)

    def toggle_current_image_favorite(self):
        """Thêm hoặc bỏ yêu thích nhanh cho ảnh đang trình chiếu khi bấm nút ❤️ ở góc"""
        path = self.image_manager.get_current_path()
        if not path:
            return

        favorites = self.settings.get("favorites", [])
        if path in favorites:
            favorites.remove(path)
        else:
            favorites.append(path)
        
        self.settings["favorites"] = favorites
        save_settings(self.settings)

        # Cập nhật lại giao diện nút ngay lập tức
        self.update_favorite_button_state()

    def closeEvent(self, event):
        """Lưu lại vị trí, kích thước và trạng thái hiển thị trước khi tắt app"""
        # Lưu lại tọa độ ở trạng thái bình thường (kể cả khi đang maximize/fullscreen)
        normal_geo = self.normalGeometry()
        self.settings["window_geometry"] = [normal_geo.x(), normal_geo.y(), normal_geo.width(), normal_geo.height()]
        
        self.settings["is_maximized"] = self.isMaximized()
        self.settings["is_fullscreen"] = self.isFullScreen()
        
        save_settings(self.settings)
        event.accept()
