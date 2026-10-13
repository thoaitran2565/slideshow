import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox, QSplitter, QWidget,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QKeySequence, QShortcut
from src.config import load_settings, save_settings


class FavoritesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bộ Sưu Tập Ảnh Yêu Thích")
        self.resize(900, 600)
        self.settings = load_settings()
        self.current_pixmap = QPixmap()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QListWidget {
                background-color: #222222;
                border: 1px solid #444;
                border-radius: 6px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #00adb5;
                color: black;
            }
            QLineEdit {
                background-color: #222222;
                border: 1px solid #555;
                border-radius: 4px;
                color: white;
                padding: 6px;
            }
            QPushButton {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00adb5;
                color: black;
                border-color: #00adb5;
            }
            QPushButton#btnAdd {
                background-color: #00adb5;
                color: black;
            }
            QPushButton#btnAdd:hover {
                background-color: #008891;
                color: white;
            }
            QPushButton#btnDanger:hover {
                background-color: #d9534f;
                border-color: #d9534f;
                color: white;
            }
            QLabel {
                color: #ddd;
            }
        """)

        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # CỘT TRÁI: Danh sách tên file ảnh yêu thích & Khung thêm đường dẫn thủ công
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(QLabel("Danh sách ảnh yêu thích:"))
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.list_widget)

        # Khung nhập và thêm đường dẫn ảnh thủ công
        add_layout = QHBoxLayout()
        self.txt_path_input = QLineEdit()
        self.txt_path_input.setPlaceholderText("Dán đường dẫn tệp ảnh vào đây...")
        
        btn_add = QPushButton("Thêm")
        btn_add.setObjectName("btnAdd")
        btn_add.clicked.connect(self.add_manual_favorite)
        
        add_layout.addWidget(self.txt_path_input)
        add_layout.addWidget(btn_add)
        left_layout.addLayout(add_layout)

        btn_remove = QPushButton("💔 Xóa Khỏi Yêu Thích")
        btn_remove.setObjectName("btnDanger")
        btn_remove.clicked.connect(self.remove_from_favorites)
        left_layout.addWidget(btn_remove)

        splitter.addWidget(left_widget)

        # CỘT PHẢI: Khu vực xem trước ảnh & Các nút điều khiển
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Header phải: Tiêu đề + Nút Fullscreen
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Xem trước:"))
        header_layout.addStretch()
        
        self.btn_fullscreen = QPushButton("⛶ Toàn Màn Hình")
        self.btn_fullscreen.clicked.connect(self.toggle_fullscreen)
        header_layout.addWidget(self.btn_fullscreen)
        right_layout.addLayout(header_layout)

        # Container chứa Ảnh (Dùng QWidget làm cha để đặt 2 nút mũi tên đè lên 2 bên)
        self.image_container = QWidget(self)
        self.image_container.setStyleSheet("background-color: #111; border: 1px solid #333; border-radius: 6px;")
        container_layout = QVBoxLayout(self.image_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("border: none; background: transparent;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Cho phép kéo di chuyển ảnh khi phóng to
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        container_layout.addWidget(self.view)

        right_layout.addWidget(self.image_container, stretch=1)

        # Style cho 2 nút mũi tên nổi 2 bên (overlay button)
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

        # 2 nút mũi tên Trái & Phải nằm nổi trên container ảnh
        self.btn_side_prev = QPushButton("◄", self.image_container)
        self.btn_side_next = QPushButton("►", self.image_container)
        self.btn_side_prev.setStyleSheet(style_overlay_btn)
        self.btn_side_next.setStyleSheet(style_overlay_btn)
        self.btn_side_prev.clicked.connect(self.prev_image)
        self.btn_side_next.clicked.connect(self.next_image)

        splitter.addWidget(right_widget)
        splitter.setSizes([280, 620])

        main_layout.addWidget(splitter)

        # Phím tắt điều hướng nhanh trong trang yêu thích
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self.prev_image)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self.next_image)
        QShortcut(QKeySequence(Qt.Key.Key_F11), self, self.toggle_fullscreen)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self.exit_fullscreen)

        self.load_favorites_list()
        
        # Dùng Timer ngắn để định vị lại nút ngay sau khi cửa sổ render hoàn tất lần đầu
        QTimer.singleShot(50, self.update_nav_buttons_position)

    def load_favorites_list(self):
        self.list_widget.clear()
        favorites = self.settings.get("favorites", [])
        
        for path in favorites:
            if os.path.exists(path):
                filename = os.path.basename(path)
                item = QListWidgetItem(filename)
                item.setData(Qt.ItemDataRole.UserRole, path)
                self.list_widget.addItem(item)
            
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
        else:
            self.pixmap_item.setPixmap(QPixmap())
            self.current_pixmap = QPixmap()

    def on_selection_changed(self, row):
        if row < 0:
            self.pixmap_item.setPixmap(QPixmap())
            self.current_pixmap = QPixmap()
            return
        item = self.list_widget.item(row)
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            if os.path.exists(path):
                self.current_pixmap = QPixmap(path)
                self.pixmap_item.setPixmap(self.current_pixmap)
                self.scene.setSceneRect(self.pixmap_item.boundingRect())
                self.fit_image_in_view()

    def fit_image_in_view(self):
        if not self.current_pixmap.isNull():
            self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def update_nav_buttons_position(self):
        """Cố định vị trí chuẩn của 2 nút next/prev ở 2 bên giữa khung ảnh"""
        btn_size = 38
        container_w = self.image_container.width()
        container_h = self.image_container.height()
        
        if container_w > 50 and container_h > 50:
            self.btn_side_prev.setGeometry(15, (container_h - btn_size) // 2, btn_size, btn_size)
            self.btn_side_next.setGeometry(container_w - btn_size - 15, (container_h - btn_size) // 2, btn_size, btn_size)
            self.btn_side_prev.raise_()
            self.btn_side_next.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_image_in_view()
        self.update_nav_buttons_position()

    def wheelEvent(self, event):
        """Tính năng phóng to / thu nhỏ ảnh khi lăn chuột"""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.view.scale(zoom_factor, zoom_factor)

    def prev_image(self):
        count = self.list_widget.count()
        if count == 0:
            return
        curr = self.list_widget.currentRow()
        new_row = (curr - 1) % count
        self.list_widget.setCurrentRow(new_row)

    def next_image(self):
        count = self.list_widget.count()
        if count == 0:
            return
        curr = self.list_widget.currentRow()
        new_row = (curr + 1) % count
        self.list_widget.setCurrentRow(new_row)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.btn_fullscreen.setText("⛶ Toàn Màn Hình")
        else:
            self.showFullScreen()
            self.btn_fullscreen.setText("🗗 Thu Nhỏ")
        QTimer.singleShot(50, self.update_nav_buttons_position)

    def exit_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.btn_fullscreen.setText("⛶ Toàn Màn Hình")
            QTimer.singleShot(50, self.update_nav_buttons_position)

    def add_manual_favorite(self):
        path = self.txt_path_input.text().strip()
        path = path.strip('"').strip("'")

        if not path:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đường dẫn tệp ảnh!")
            return

        if not os.path.exists(path):
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy đường dẫn tệp:\n{path}")
            return

        favorites = self.settings.get("favorites", [])
        if path in favorites:
            QMessageBox.information(self, "Thông báo", "Ảnh này đã có sẵn trong danh sách yêu thích.")
            return

        favorites.append(path)
        self.settings["favorites"] = favorites
        save_settings(self.settings)

        self.txt_path_input.clear()
        self.load_favorites_list()
        QMessageBox.information(self, "Thành công", "Đã thêm ảnh vào danh sách yêu thích thành công! ❤️")

    def remove_from_favorites(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        item = self.list_widget.item(row)
        path = item.data(Qt.ItemDataRole.UserRole)

        favorites = self.settings.get("favorites", [])
        if path in favorites:
            favorites.remove(path)
            self.settings["favorites"] = favorites
            save_settings(self.settings)
            self.load_favorites_list()
            QMessageBox.information(self, "Thành công", "Đã xóa ảnh khỏi danh sách yêu thích.")