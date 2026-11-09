import os
from typing import Optional
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QColor, QKeySequence, QShortcut, QAction, QBrush, QIcon, QMouseEvent, QTransform
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QColorDialog, QMenu, QMessageBox, QApplication,
    QPushButton, QGraphicsOpacityEffect, QLabel, QGraphicsDropShadowEffect
)

from src.presentation.presenter import ViewerPresenter
from src.presentation.views.control_panel import ControlPanel, BackdropOverlay
from src.presentation.views.settings_dialog import SettingsDialog
from src.presentation.views.favorites_window import FavoritesWindow
from src.infrastructure.path_utils import get_resource_path
from src.domain.models import TransitionType, BgmPlaybackState
from src.presentation.views.transitions.engine import TransitionEngine
from src.presentation.views.transitions.fade_transition import CrossFadeTransition
from src.presentation.views.transitions.slide_transition import SlideTransition
from src.presentation.views.transitions.zoom_transition import ZoomFadeTransition
from src.presentation.views.transitions.instant_transition import InstantTransition


class PhotoViewerWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng xem và trình chiếu ảnh."""
    def __init__(self, presenter: ViewerPresenter, start_file: str = None):
        super().__init__()
        self.presenter = presenter

        # Nạp ảnh với folder trong cấu hình
        initial_folder = self.presenter.settings.image_folder or "images"
        self.presenter.load_initial_images(folder=initial_folder, start_file=start_file)

        self.interval_ms = self.presenter.settings.interval_ms
        self.bg_color = QColor(self.presenter.settings.bg_color)
        self.is_playing = True

        # Trạng thái điều khiển phóng đại (Zoom State)
        self.current_zoom = 1.0
        self.min_zoom = 1.0
        self.max_zoom = 20.0
        self.zoom_step = 1.15

        self.init_ui()

        # Khôi phục vị trí và trạng thái cửa sổ
        saved_geo = self.presenter.settings.window_geometry
        if saved_geo and len(saved_geo) == 4:
            self.setGeometry(saved_geo[0], saved_geo[1], saved_geo[2], saved_geo[3])

        if self.presenter.settings.is_maximized:
            self.showMaximized()
        elif self.presenter.settings.is_fullscreen:
            self.showFullScreen()

        self.show_image()

        # Timer trình chiếu tự động
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image_auto)
        if self.presenter.playlist.total_count > 0:
            self.timer.start(self.interval_ms)

        # Timer phân biệt Click đơn (Pause/Play) và Click đúp (Fullscreen)
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.toggle_play_pause)

    def init_ui(self):
        self.setWindowTitle("Windows Photo Slideshow")
        self.resize(1050, 720)

        icon_path = get_resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

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
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.view.installEventFilter(self)
        self.view.viewport().installEventFilter(self)
        self.main_layout.addWidget(self.view)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # Incoming pixmap item phục vụ cho các hiệu ứng chuyển cảnh
        self.incoming_pixmap_item = QGraphicsPixmapItem()
        self.incoming_pixmap_item.setVisible(False)
        self.scene.addItem(self.incoming_pixmap_item)

        # Khởi tạo bộ điều phối hiệu ứng chuyển cảnh (Transition Engine)
        self.transition_engine = TransitionEngine()
        self.transition_engine.register_strategy(TransitionType.FADE, CrossFadeTransition())
        self.transition_engine.register_strategy(TransitionType.SLIDE_LEFT, SlideTransition(slide_to_left=True))
        self.transition_engine.register_strategy(TransitionType.SLIDE_RIGHT, SlideTransition(slide_to_left=False))
        self.transition_engine.register_strategy(TransitionType.ZOOM_FADE, ZoomFadeTransition())
        self.transition_engine.register_strategy(TransitionType.NONE, InstantTransition())

        # Hiệu ứng Fade In / Fade Out khi đổi ảnh
        self.opacity_effect = QGraphicsOpacityEffect(self.view)
        self.view.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(350)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Style nút nổi overlay
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

        # 4. Nút hiện lại thanh công cụ khi bị ẩn (tương phản cao + Drop Shadow)
        self.btn_show_panel = QPushButton("👁️ Hiện thanh công cụ", self)
        self.btn_show_panel.setStyleSheet("""
            QPushButton {
                background-color: rgba(18, 18, 18, 245);
                color: #FFFFFF;
                border-radius: 12px;
                padding: 8px 18px;
                border: 2px solid rgba(255, 255, 255, 120);
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #00adb5;
                color: #000000;
                border-color: #00adb5;
            }
        """)
        shadow_btn = QGraphicsDropShadowEffect(self.btn_show_panel)
        shadow_btn.setBlurRadius(20)
        shadow_btn.setOffset(0, 4)
        shadow_btn.setColor(QColor(0, 0, 0, 210))
        self.btn_show_panel.setGraphicsEffect(shadow_btn)
        self.btn_show_panel.hide()
        self.btn_show_panel.clicked.connect(self.toggle_control_panel)

        # 5. Thanh công cụ bên dưới & Lớp phủ chống click xuyên
        self.backdrop_overlay = BackdropOverlay(self)
        self.control_panel = ControlPanel(self)
        self.control_panel.btn_play_pause.clicked.connect(self.toggle_play_pause)
        self.control_panel.btn_random.toggled.connect(self.toggle_random)
        self.control_panel.btn_rotate.clicked.connect(self.rotate_image_cw)
        self.control_panel.btn_bgm.clicked.connect(self.toggle_bgm_action)
        self.control_panel.bgm_volume_changed.connect(lambda v: self.presenter.set_bgm_volume(v, persist=False))
        self.control_panel.bgm_volume_saved.connect(lambda v: self.presenter.persist_bgm_volume(v))
        self.control_panel.btn_color.clicked.connect(self.change_bg_color)
        self.control_panel.btn_hide.clicked.connect(self.toggle_control_panel)

        self.control_panel.set_interval_value(self.interval_ms // 1000)
        self.control_panel.interval_changed.connect(self.on_interval_changed)
        self.presenter.set_bgm_state_callback(self.on_bgm_state_changed)
        self.update_bgm_button_state()

        # Khôi phục trạng thái Random từ cấu hình
        if self.presenter.settings.is_random:
            self.control_panel.btn_random.setChecked(True)

        # Khôi phục trạng thái Ẩn/Hiện thanh công cụ từ cấu hình
        if not self.presenter.settings.show_control_panel:
            self.control_panel.hide()
            self.btn_show_panel.show()
        else:
            self.control_panel.show()
            self.btn_show_panel.hide()

        # Phím tắt điều hướng & điều khiển
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self.prev_image_manual)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self.next_image_manual)
        QShortcut(QKeySequence(Qt.Key.Key_Space), self, self.toggle_play_pause)
        QShortcut(QKeySequence(Qt.Key.Key_F11), self, self.toggle_fullscreen)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self.exit_fullscreen)
        QShortcut(QKeySequence(Qt.Key.Key_H), self, self.toggle_control_panel)

        # Phím tắt xoay & lật ảnh (Ergonomic Shortcuts)
        QShortcut(QKeySequence(Qt.Key.Key_R), self, self.rotate_image_cw)
        QShortcut(QKeySequence("Shift+R"), self, self.rotate_image_ccw)
        QShortcut(QKeySequence(Qt.Key.Key_F), self, self.flip_image_h)
        QShortcut(QKeySequence(Qt.Key.Key_V), self, self.flip_image_v)
        QShortcut(QKeySequence("Ctrl+R"), self, self.reset_image_transform)

        self.update_background()

    def eventFilter(self, watched, event):
        """Bắt sự kiện chuột trên viewport của QGraphicsView."""
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
            elif event.type() == event.Type.Wheel:
                self.handle_wheel_zoom(event)
                return True
        return super().eventFilter(watched, event)

    def reload_and_show(self):
        count = self.presenter.reload_images()
        if count > 0:
            self.show_image()
        else:
            self.scene.clear()
            self.lbl_top_info.setText(self.presenter.get_info_text())

    def show_image(self, direction="forward"):
        item = self.presenter.get_current_item()
        if not item or not os.path.exists(item.path):
            self.lbl_top_info.setText(self.presenter.get_info_text())
            return

        pixmap = QPixmap(item.path)
        if not pixmap.isNull():
            trans_type = self.presenter.get_transition_type()

            def _after_transition():
                self.apply_current_transform()
                self.lbl_top_info.setText(self.presenter.get_info_text())
                self.lbl_top_info.adjustSize()
                self.update_favorite_button_state()

            # Nếu là lần nạp ảnh đầu tiên (pixmap_item đang rỗng):
            if self.pixmap_item.pixmap().isNull():
                self.pixmap_item.setPixmap(pixmap)
                _after_transition()
            else:
                self.transition_engine.perform_transition(
                    transition_type=trans_type,
                    view=self.view,
                    current_item=self.pixmap_item,
                    incoming_item=self.incoming_pixmap_item,
                    next_pixmap=pixmap,
                    direction=direction,
                    duration_ms=450,
                    on_finished=_after_transition
                )

        self.update_bgm_button_state()

    def fit_image_in_view(self):
        self.current_zoom = 1.0
        if not self.pixmap_item.pixmap().isNull():
            self.view.resetTransform()
            scene_bounds = self.pixmap_item.mapToScene(self.pixmap_item.boundingRect()).boundingRect()
            if not scene_bounds.isEmpty():
                self.view.fitInView(scene_bounds, Qt.AspectRatioMode.KeepAspectRatio)
            else:
                self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)

    def apply_current_transform(self):
        """Áp dụng góc xoay và lật từ bộ nhớ đệm phiên lên pixmap_item."""
        transform_state = self.presenter.get_current_transform()
        if not self.pixmap_item.pixmap().isNull():
            rect = self.pixmap_item.boundingRect()
            cx, cy = rect.width() / 2, rect.height() / 2
            t = QTransform()
            t.translate(cx, cy)
            t.rotate(transform_state.rotation_degrees)
            sx = -1 if transform_state.flip_h else 1
            sy = -1 if transform_state.flip_v else 1
            t.scale(sx, sy)
            t.translate(-cx, -cy)
            self.pixmap_item.setTransform(t)

            scene_bounds = self.pixmap_item.mapToScene(self.pixmap_item.boundingRect()).boundingRect()
            self.scene.setSceneRect(scene_bounds)
            self.fit_image_in_view()

    def rotate_image_cw(self):
        self.presenter.rotate_current(clockwise=True)
        self.apply_current_transform()

    def rotate_image_ccw(self):
        self.presenter.rotate_current(clockwise=False)
        self.apply_current_transform()

    def flip_image_h(self):
        self.presenter.flip_current_h()
        self.apply_current_transform()

    def flip_image_v(self):
        self.presenter.flip_current_v()
        self.apply_current_transform()

    def reset_image_transform(self):
        self.presenter.reset_current_transform()
        self.apply_current_transform()

    def on_bgm_state_changed(self, state, msg: Optional[str] = None):
        if state == BgmPlaybackState.LOADING:
            self.control_panel.set_bgm_loading(True)
        elif state == BgmPlaybackState.ERROR:
            self.control_panel.set_bgm_loading(False, error_msg=msg)
            self.update_bgm_button_state()
        elif state == BgmPlaybackState.PLAYING:
            self.control_panel.set_bgm_loading(False)
            self.update_bgm_button_state()
        elif state == BgmPlaybackState.STOPPED:
            self.control_panel.set_bgm_loading(False)
            self.update_bgm_button_state()

    def update_bgm_button_state(self):
        is_ready = self.presenter.is_bgm_ready()
        is_playing = self.presenter.is_bgm_playing()
        self.control_panel.set_bgm_state(is_ready, is_playing)
        self.control_panel.set_current_bgm_volume(self.presenter.settings.bgm_volume)

    def toggle_bgm_action(self):
        if not self.presenter.is_bgm_ready():
            self.open_settings()
        else:
            if self.presenter.is_bgm_playing():
                self.presenter.stop_bgm()
                self.update_bgm_button_state()
            else:
                self.presenter.play_bgm()

    def next_image_manual(self):
        self.presenter.next_image()
        self.show_image(direction="forward")
        if self.is_playing:
            self.timer.start(self.interval_ms)

    def prev_image_manual(self):
        self.presenter.prev_image()
        self.show_image(direction="backward")
        if self.is_playing:
            self.timer.start(self.interval_ms)

    def next_image_auto(self):
        if self.is_playing:
            self.presenter.next_image()
            self.show_image(direction="forward")

    def toggle_play_pause(self):
        self.is_playing = not self.is_playing
        self.control_panel.set_play_state(self.is_playing)
        if self.is_playing:
            self.timer.start(self.interval_ms)
        else:
            self.timer.stop()

    def toggle_random(self, checked: bool):
        self.presenter.set_random(checked)
        self.lbl_top_info.setText(self.presenter.get_info_text())
        self.lbl_top_info.adjustSize()

    def on_interval_changed(self, seconds: int):
        self.interval_ms = self.presenter.update_interval(seconds)
        if self.is_playing:
            self.timer.start(self.interval_ms)

    def change_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self, "Chọn màu nền trình chiếu")
        if color.isValid():
            self.bg_color = color
            self.update_background()
            self.presenter.update_bg_color(color.name())

    def update_background(self):
        brush = QBrush(self.bg_color)
        self.scene.setBackgroundBrush(brush)
        self.view.setBackgroundBrush(brush)
        self.view.viewport().setStyleSheet(f"background-color: {self.bg_color.name()};")

    def toggle_control_panel(self):
        if self.control_panel.isVisible():
            self.control_panel.hide()
            self.btn_show_panel.show()
            self.presenter.set_control_panel_visibility(False)
        else:
            self.control_panel.show()
            self.btn_show_panel.hide()
            self.presenter.set_control_panel_visibility(True)

    def open_settings(self):
        was_playing = self.is_playing
        if was_playing:
            self.timer.stop()

        dialog = SettingsDialog(self, presenter=self.presenter)
        if dialog.exec():
            new_folder = dialog.settings.image_folder
            if new_folder != self.presenter.settings.image_folder:
                self.presenter.settings.image_folder = new_folder
                self.reload_and_show()
            self.update_bgm_button_state()

        if was_playing and self.presenter.playlist.total_count > 0:
            self.timer.start(self.interval_ms)

    def open_favorites_window(self):
        was_playing = self.is_playing
        if was_playing:
            self.timer.stop()

        fav_win = FavoritesWindow(self)
        fav_win.exec()

        if was_playing and self.presenter.playlist.total_count > 0:
            self.timer.start(self.interval_ms)

    def show_options_menu(self):
        curr_path = self.presenter.get_current_path()
        if not curr_path:
            return

        was_playing = self.is_playing
        if was_playing:
            self.timer.stop()

        menu = QMenu(self)

        is_fav = self.presenter.is_current_favorite()
        fav_label = "❤️ Bỏ Yêu Thích" if is_fav else "🤍 Thêm Vào Yêu Thích"

        act_fav = QAction(fav_label, self)
        act_fav.triggered.connect(self.toggle_current_image_favorite)

        act_rotate_cw = QAction("🔄 Xoay Phải 90° (R)", self)
        act_rotate_cw.triggered.connect(self.rotate_image_cw)

        act_rotate_ccw = QAction("↺ Xoay Trái 90° (Shift+R)", self)
        act_rotate_ccw.triggered.connect(self.rotate_image_ccw)

        act_flip_h = QAction("↔️ Lật Ngang (F)", self)
        act_flip_h.triggered.connect(self.flip_image_h)

        act_flip_v = QAction("↕️ Lật Dọc (V)", self)
        act_flip_v.triggered.connect(self.flip_image_v)

        act_reset_transform = QAction("⏮ Đặt Lại Góc Ảnh (Ctrl+R)", self)
        act_reset_transform.triggered.connect(self.reset_image_transform)

        act_copy_file = QAction("📋 Copy Đường Dẫn Tệp Ảnh", self)
        act_copy_file.triggered.connect(lambda: QApplication.clipboard().setText(curr_path))

        act_open_folder = QAction("📁 Mở Trong Thư Mục (Explorer)", self)
        act_open_folder.triggered.connect(lambda: self.presenter.reveal_in_explorer())

        act_delete = QAction("🗑️ Xóa Ảnh (Vào Thùng Rác)", self)
        act_delete.triggered.connect(self.delete_current_image)

        menu.addAction(act_fav)
        menu.addSeparator()
        menu.addAction(act_rotate_cw)
        menu.addAction(act_rotate_ccw)
        menu.addAction(act_flip_h)
        menu.addAction(act_flip_v)
        menu.addAction(act_reset_transform)
        menu.addSeparator()
        menu.addAction(act_copy_file)
        menu.addAction(act_open_folder)
        menu.addSeparator()
        menu.addAction(act_delete)

        menu.exec(self.btn_top_option.mapToGlobal(QPoint(0, self.btn_top_option.height() + 5)))

        if was_playing and self.presenter.playlist.total_count > 0:
            self.timer.start(self.interval_ms)

    def delete_current_image(self):
        curr_path = self.presenter.get_current_path()
        if not curr_path:
            return

        reply = QMessageBox.question(
            self, 'Xác nhận xóa',
            f"Bạn có chắc muốn chuyển file này vào thùng rác?\n{os.path.basename(curr_path)}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message, next_item = self.presenter.delete_current_image()
            if success:
                if next_item:
                    self.show_image()
                else:
                    self.scene.clear()
                    self.lbl_top_info.setText(self.presenter.get_info_text())

    def toggle_current_image_favorite(self):
        self.presenter.toggle_favorite()
        self.update_favorite_button_state()

    def update_favorite_button_state(self):
        is_fav = self.presenter.is_current_favorite()
        if is_fav:
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
                QPushButton:hover { background-color: rgba(50, 50, 50, 230); }
            """)
        else:
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

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def exit_fullscreen(self):
        if hasattr(self, 'backdrop_overlay') and self.backdrop_overlay and self.backdrop_overlay.isVisible():
            self.backdrop_overlay.dismissed.emit()
            return
        if self.isFullScreen():
            self.showNormal()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_image_in_view()
        if hasattr(self, 'backdrop_overlay') and self.backdrop_overlay:
            self.backdrop_overlay.setGeometry(self.rect())

        btn_size = 38
        self.lbl_top_info.move(20, 20)
        self.btn_top_option.setGeometry(self.width() - btn_size - 20, 20, btn_size, btn_size)
        self.btn_top_settings.setGeometry(self.width() - (btn_size * 2) - 30, 20, btn_size, btn_size)
        self.btn_top_favorites.setGeometry(self.width() - (btn_size * 3) - 40, 20, btn_size, btn_size)

        self.btn_side_prev.setGeometry(20, (self.height() - btn_size) // 2, btn_size, btn_size)
        self.btn_side_next.setGeometry(self.width() - btn_size - 20, (self.height() - btn_size) // 2, btn_size, btn_size)

        self.btn_show_panel.setGeometry((self.width() - 170) // 2, self.height() - 55, 170, 38)

        panel_width = 760
        panel_height = 48
        self.control_panel.setGeometry(
            (self.width() - panel_width) // 2,
            self.height() - panel_height - 25,
            panel_width,
            panel_height
        )

    def handle_wheel_zoom(self, event):
        delta = event.angleDelta().y()
        if delta == 0:
            return

        if delta > 0:
            # Phóng to (Zoom In)
            if self.current_zoom >= self.max_zoom:
                return
            new_zoom = self.current_zoom * self.zoom_step
            if new_zoom > self.max_zoom:
                factor = self.max_zoom / self.current_zoom
                self.current_zoom = self.max_zoom
            else:
                factor = self.zoom_step
                self.current_zoom = new_zoom

            self.view.scale(factor, factor)
            self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        else:
            # Thu nhỏ (Zoom Out)
            if self.current_zoom <= 1.001:
                # No-op: Không thu nhỏ dưới kích thước vừa vặn ban đầu
                return
            new_zoom = self.current_zoom / self.zoom_step
            if new_zoom <= 1.001:
                # Kẹp về kích thước vừa khít ban đầu và căn giữa
                self.fit_image_in_view()
            else:
                factor = 1.0 / self.zoom_step
                self.current_zoom = new_zoom
                self.view.scale(factor, factor)

    def wheelEvent(self, event):
        self.handle_wheel_zoom(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            child = self.childAt(event.pos())
            if child in (self.view, self.central_widget, self.view.viewport()):
                self.click_timer.start(220)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.click_timer.isActive():
                self.click_timer.stop()
            self.toggle_fullscreen()
        super().mouseDoubleClickEvent(event)

    def closeEvent(self, event):
        self.presenter.stop_bgm()
        normal_geo = self.normalGeometry()
        geo_list = [normal_geo.x(), normal_geo.y(), normal_geo.width(), normal_geo.height()]
        self.presenter.save_window_state(
            geometry=geo_list,
            is_maximized=self.isMaximized(),
            is_fullscreen=self.isFullScreen()
        )
        event.accept()

