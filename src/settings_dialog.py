import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QComboBox, QCheckBox, QTabWidget, QWidget, QMessageBox
)
from src.config import load_settings, save_settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài Đặt Hệ Thống")
        self.setMinimumSize(480, 380)
        self.settings = load_settings()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # TAB 1: Cấu hình Chung (Chọn thư mục)
        tab_general = QWidget()
        gen_layout = QVBoxLayout(tab_general)

        gen_layout.addWidget(QLabel("Thư mục chứa ảnh trình chiếu:"))
        folder_layout = QHBoxLayout()
        self.txt_folder = QLabel(self.settings.get("image_folder", "Chưa chọn thư mục"))
        self.txt_folder.setStyleSheet("padding: 6px; border: 1px solid #555; border-radius: 4px; background: #222; color: #fff;")
        btn_browse = QPushButton("Chọn...")
        btn_browse.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.txt_folder)
        folder_layout.addWidget(btn_browse)
        gen_layout.addLayout(folder_layout)

        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Thời gian mỗi ảnh (giây):"))
        self.spn_interval = QSpinBox()
        self.spn_interval.setRange(1, 60)
        self.spn_interval.setValue(self.settings.get("interval_ms", 3000) // 1000)
        time_layout.addWidget(self.spn_interval)
        gen_layout.addLayout(time_layout)

        gen_layout.addStretch()
        tabs.addTab(tab_general, "Trình Chiếu")

        # Thêm nút mở trang Ảnh Yêu Thích vào tab Cài đặt chung
        btn_open_favs = QPushButton("❤️ Xem & Quản Lý Ảnh Yêu Thích")
        btn_open_favs.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold; padding: 6px;")
        btn_open_favs.clicked.connect(self.open_favorites_window)
        gen_layout.addWidget(btn_open_favs)

        # TAB 2: Hiệu Ứng & Giao Diện
        tab_effects = QWidget()
        eff_layout = QVBoxLayout(tab_effects)

        eff_layout.addWidget(QLabel("Hiệu ứng chuyển cảnh:"))
        self.cmb_effect = QComboBox()
        self.cmb_effect.addItems(["Fade In/Out", "Slide Right (Đang cập nhật)", "Zoom (Đang cập nhật)"])
        eff_layout.addWidget(self.cmb_effect)

        self.chk_dark = QCheckBox("Giao diện tối (Dark Mode)")
        self.chk_dark.setChecked(True)
        eff_layout.addWidget(self.chk_dark)

        eff_layout.addStretch()
        tabs.addTab(tab_effects, "Giao Diện")

        # TAB 3: Nâng Cao
        tab_adv = QWidget()
        adv_layout = QVBoxLayout(tab_adv)
        adv_layout.addWidget(QLabel("Tự động quét ảnh thư mục con: (Đang cập nhật)"))
        adv_layout.addWidget(QLabel("Đồng bộ Google Drive: (Đang cập nhật)"))
        adv_layout.addWidget(QLabel("Chế độ xem Ultra-HD AI: (Đang cập nhật)"))
        adv_layout.addStretch()
        tabs.addTab(tab_adv, "Nâng Cao")

        main_layout.addWidget(tabs)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Lưu Cài Đặt")
        btn_save.setStyleSheet("background-color: #00adb5; color: white; font-weight: bold; padding: 6px 16px;")
        btn_save.clicked.connect(self.save_data)
        
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        main_layout.addLayout(btn_layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục ảnh", self.txt_folder.text())
        if folder:
            self.txt_folder.setText(folder)

    def save_data(self):
        folder = self.txt_folder.text()
        if not folder or folder == "Chưa chọn thư mục" or not os.path.exists(folder):
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thư mục ảnh hợp lệ!")
            return

        self.settings["image_folder"] = folder
        self.settings["interval_ms"] = self.spn_interval.value() * 1000
        save_settings(self.settings)
        self.accept()
        
    def open_favorites_window(self):
        self.accept()  # Đóng cửa sổ Cài đặt hiện tại
        
        from src.favorites_window import FavoritesWindow
        # Lấy cửa sổ chính (PhotoViewerWindow) làm parent để mở trang yêu thích
        fav_win = FavoritesWindow(self.parent())
        fav_win.exec()