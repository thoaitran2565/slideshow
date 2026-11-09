import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox, QSplitter, QWidget,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from src.infrastructure.json_settings_repo import JsonSettingsRepository
from src.infrastructure.path_utils import get_resource_path


class FavoritesWindow(QDialog):
    """Cửa sổ xem và quản lý danh sách ảnh yêu thích."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bộ Sưu Tập Ảnh Yêu Thích")
        self.resize(900, 600)

        icon_path = get_resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.settings_repo = JsonSettingsRepository()
        self.settings = self.settings_repo.load_settings()
        self.current_pixmap = QPixmap()
        self.init_ui()
        self.load_favorites_list()

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

        # Cột trái: Danh sách ảnh
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(QLabel("Danh sách ảnh yêu thích:"))
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.list_widget)

        # Khung nhập đường dẫn thủ công
        add_layout = QHBoxLayout()
        self.txt_path_input = QLineEdit()
        self.txt_path_input.setPlaceholderText("Dán đường dẫn tệp ảnh vào đây...")
        btn_add = QPushButton("Thêm")
        btn_add.setObjectName("btnAdd")
        btn_add.clicked.connect(self.add_manual_path)
        add_layout.addWidget(self.txt_path_input)
        add_layout.addWidget(btn_add)
        left_layout.addLayout(add_layout)

        # Cụm nút thao tác
        action_layout = QHBoxLayout()
        btn_remove = QPushButton("Bỏ Yêu Thích")
        btn_remove.setObjectName("btnDanger")
        btn_remove.clicked.connect(self.remove_selected_favorite)
        btn_open_folder = QPushButton("Mở Thư Mục")
        btn_open_folder.clicked.connect(self.open_in_explorer)
        action_layout.addWidget(btn_remove)
        action_layout.addWidget(btn_open_folder)
        left_layout.addLayout(action_layout)

        splitter.addWidget(left_widget)

        # Cột phải: Xem trước ảnh
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_preview_title = QLabel("Xem trước ảnh:")
        right_layout.addWidget(self.lbl_preview_title)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("border: 1px solid #444; background-color: #111;")
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        right_layout.addWidget(self.view)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

    def load_favorites_list(self):
        self.list_widget.clear()
        self.settings = self.settings_repo.load_settings()
        for path in self.settings.favorites:
            name = os.path.basename(path)
            item = QListWidgetItem(f"❤️ {name}")
            item.setData(Qt.ItemDataRole.UserRole, path)
            self.list_widget.addItem(item)

        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def on_selection_changed(self, row: int):
        if row < 0:
            self.pixmap_item.setPixmap(QPixmap())
            return
        item = self.list_widget.item(row)
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if os.path.exists(path):
            pixmap = QPixmap(path)
            self.pixmap_item.setPixmap(pixmap)
            self.scene.setSceneRect(self.pixmap_item.boundingRect())
            self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
            self.lbl_preview_title.setText(f"Xem trước: {os.path.basename(path)}")
        else:
            self.pixmap_item.setPixmap(QPixmap())
            self.lbl_preview_title.setText(f"[Tệp không tồn tại] {os.path.basename(path)}")

    def add_manual_path(self):
        path = self.txt_path_input.text().strip().strip('"')
        if not path:
            return
        if not os.path.exists(path):
            QMessageBox.warning(self, "Lỗi", "Đường dẫn tệp không tồn tại!")
            return

        norm_path = os.path.normpath(path)
        if norm_path not in self.settings.favorites:
            self.settings.favorites.append(norm_path)
            self.settings_repo.save_settings(self.settings)
            self.load_favorites_list()
            self.txt_path_input.clear()
        else:
            QMessageBox.information(self, "Thông báo", "Ảnh này đã có trong danh sách yêu thích.")

    def remove_selected_favorite(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        item = self.list_widget.item(row)
        path = item.data(Qt.ItemDataRole.UserRole)

        if path in self.settings.favorites:
            self.settings.favorites.remove(path)
            self.settings_repo.save_settings(self.settings)
            self.load_favorites_list()

    def open_in_explorer(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        item = self.list_widget.item(row)
        path = item.data(Qt.ItemDataRole.UserRole)
        if path and os.path.exists(path):
            os.system(f'explorer /select,"{os.path.normpath(path)}"')

