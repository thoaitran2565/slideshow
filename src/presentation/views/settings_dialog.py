import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QComboBox, QCheckBox, QTabWidget, QWidget, QMessageBox,
    QLineEdit, QSlider
)
from src.infrastructure.json_settings_repo import JsonSettingsRepository
from src.presentation.views.favorites_window import FavoritesWindow
from src.domain.models import TransitionType


class SettingsDialog(QDialog):
    """Hộp thoại cấu hình hệ thống."""
    def __init__(self, parent=None, presenter=None):
        super().__init__(parent)
        self.setWindowTitle("Cài Đặt Hệ Thống")
        self.setMinimumSize(520, 420)
        self.presenter = presenter or getattr(parent, 'presenter', None)
        self.is_testing_audio = False

        self.settings_repo = JsonSettingsRepository()
        self.settings = self.settings_repo.load_settings()
        self.initial_youtube_url = (self.settings.bgm_youtube_url or "").strip()
        self.initial_bgm_source = self.settings.bgm_source or "youtube"
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # TAB 1: Cấu hình Chung (Chọn thư mục)
        tab_general = QWidget()
        gen_layout = QVBoxLayout(tab_general)

        gen_layout.addWidget(QLabel("Thư mục chứa ảnh trình chiếu:"))
        folder_layout = QHBoxLayout()
        current_folder = self.settings.image_folder or "Chưa chọn thư mục"
        self.txt_folder = QLabel(current_folder)
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
        self.spn_interval.setValue(self.settings.interval_ms // 1000)
        time_layout.addWidget(self.spn_interval)
        gen_layout.addLayout(time_layout)

        gen_layout.addStretch()
        tabs.addTab(tab_general, "Trình Chiếu")

        btn_open_favs = QPushButton("❤️ Xem & Quản Lý Ảnh Yêu Thích")
        btn_open_favs.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold; padding: 6px;")
        btn_open_favs.clicked.connect(self.open_favorites_window)
        gen_layout.addWidget(btn_open_favs)

        # TAB 2: Nhạc Nền (BGM)
        tab_bgm = QWidget()
        bgm_layout = QVBoxLayout(tab_bgm)

        bgm_layout.addWidget(QLabel("Nguồn phát nhạc:"))
        self.cmb_bgm_source = QComboBox()
        self.cmb_bgm_source.addItem("YouTube (Trực tuyến)", "youtube")
        self.cmb_bgm_source.addItem("Tệp ổ cứng cục bộ (Sắp ra mắt)", "local")
        self.cmb_bgm_source.addItem("Spotify (Sắp ra mắt)", "spotify")

        # Vô hiệu hóa các nguồn chưa hỗ trợ trong model
        model = self.cmb_bgm_source.model()
        if hasattr(model, 'item'):
            for i in range(self.cmb_bgm_source.count()):
                item = model.item(i)
                if item and self.cmb_bgm_source.itemData(i) != "youtube":
                    item.setEnabled(False)

        def _on_source_changed(idx):
            if self.cmb_bgm_source.itemData(idx) != "youtube":
                self.cmb_bgm_source.setCurrentIndex(0)

        self.cmb_bgm_source.currentIndexChanged.connect(_on_source_changed)

        # Chọn đúng nguồn đã lưu (nếu hợp lệ)
        src_idx = self.cmb_bgm_source.findData(self.settings.bgm_source)
        if src_idx != -1 and self.settings.bgm_source == "youtube":
            self.cmb_bgm_source.setCurrentIndex(src_idx)
        else:
            self.cmb_bgm_source.setCurrentIndex(0)

        bgm_layout.addWidget(self.cmb_bgm_source)

        bgm_layout.addWidget(QLabel("Đường dẫn (URL) hoặc Video ID YouTube:"))
        self.txt_youtube_url = QLineEdit()
        self.txt_youtube_url.setPlaceholderText("https://www.youtube.com/watch?v=... hoặc Video ID")
        self.txt_youtube_url.setText(self.settings.bgm_youtube_url)
        self.txt_youtube_url.setStyleSheet("padding: 6px; border: 1px solid #555; border-radius: 4px; background: #222; color: #fff;")
        self.txt_youtube_url.textEdited.connect(self._on_youtube_url_edited)
        bgm_layout.addWidget(self.txt_youtube_url)

        # Hàng nút Nghe thử & Nhãn trạng thái
        test_row = QHBoxLayout()
        self.btn_test_bgm = QPushButton("▶ Nghe Thử")
        self.btn_test_bgm.setStyleSheet("background-color: #333; color: white; padding: 6px 14px; border: 1px solid #777; border-radius: 4px; font-weight: bold;")
        self.btn_test_bgm.clicked.connect(self.toggle_test_audio)
        test_row.addWidget(self.btn_test_bgm)

        self.lbl_bgm_status = QLabel("")
        self.lbl_bgm_status.setStyleSheet("font-size: 12px; color: #aaa;")
        test_row.addWidget(self.lbl_bgm_status)
        test_row.addStretch()
        bgm_layout.addLayout(test_row)

        # Âm lượng
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Âm lượng nhạc nền:"))
        self.slider_bgm_volume = QSlider(Qt.Orientation.Horizontal)
        self.slider_bgm_volume.setRange(0, 100)
        self.slider_bgm_volume.setValue(self.settings.bgm_volume)
        self.lbl_bgm_vol_val = QLabel(f"{self.settings.bgm_volume}%")
        self.slider_bgm_volume.valueChanged.connect(self._on_bgm_volume_changed)
        self.slider_bgm_volume.sliderReleased.connect(self._on_bgm_volume_released)
        vol_layout.addWidget(self.slider_bgm_volume)
        vol_layout.addWidget(self.lbl_bgm_vol_val)
        bgm_layout.addLayout(vol_layout)

        self.chk_bgm_loop = QCheckBox("Tự động lặp lại bài nhạc (Loop)")
        self.chk_bgm_loop.setChecked(self.settings.bgm_loop)
        bgm_layout.addWidget(self.chk_bgm_loop)

        bgm_layout.addStretch()
        tabs.addTab(tab_bgm, "Nhạc Nền")

        # TAB 3: Hiệu Ứng & Giao Diện
        tab_effects = QWidget()
        eff_layout = QVBoxLayout(tab_effects)

        eff_layout.addWidget(QLabel("Hiệu ứng chuyển cảnh (Slide Transitions):"))
        self.cmb_effect = QComboBox()
        self.cmb_effect.addItem("Hòa tan / Mờ dần (Cross-Fade)", TransitionType.FADE)
        self.cmb_effect.addItem("Trượt sang trái (Slide Left)", TransitionType.SLIDE_LEFT)
        self.cmb_effect.addItem("Trượt sang phải (Slide Right)", TransitionType.SLIDE_RIGHT)
        self.cmb_effect.addItem("Phóng to hòa trộn (Zoom Fade)", TransitionType.ZOOM_FADE)
        self.cmb_effect.addItem("Chuyển tức thì (Instant Cut)", TransitionType.NONE)

        # Đặt giá trị đã lưu
        idx = self.cmb_effect.findData(self.settings.transition_type)
        if idx != -1:
            self.cmb_effect.setCurrentIndex(idx)
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
        initial = self.txt_folder.text() if os.path.exists(self.txt_folder.text()) else ""
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục ảnh", initial)
        if folder:
            self.txt_folder.setText(folder)

    def _on_youtube_url_edited(self, text: str):
        if self.is_testing_audio:
            self.stop_test_audio()

    def set_bgm_loading(self, is_loading: bool, status_msg: str = ""):
        if is_loading:
            self.lbl_bgm_status.setText(status_msg or "⏳ Đang kết nối luồng nhạc...")
            self.lbl_bgm_status.setStyleSheet("color: #00adb5;")
            self.btn_test_bgm.setEnabled(False)
            self.txt_youtube_url.setEnabled(False)
        else:
            self.btn_test_bgm.setEnabled(True)
            self.txt_youtube_url.setEnabled(True)

    def toggle_test_audio(self):
        if self.is_testing_audio:
            self.stop_test_audio()
            self.lbl_bgm_status.setText("Đã dừng nghe thử.")
            self.lbl_bgm_status.setStyleSheet("color: #aaa;")
            return

        # Ngắt nhạc nền slideshow nếu đang phát ngoài màn hình chính
        if self.presenter and self.presenter.is_bgm_playing():
            self.presenter.stop_bgm()

        url = self.txt_youtube_url.text().strip()
        if not url:
            self.lbl_bgm_status.setText("⚠️ Vui lòng nhập link hoặc ID YouTube.")
            self.lbl_bgm_status.setStyleSheet("color: #ffcc00;")
            return

        self.is_testing_audio = True
        self.btn_test_bgm.setText("⏹ Dừng")
        self.lbl_bgm_status.setText("⏳ Đang kết nối luồng nhạc...")
        self.lbl_bgm_status.setStyleSheet("color: #00adb5;")

        if self.presenter and self.presenter.manage_bgm_uc:
            player = self.presenter.manage_bgm_uc.music_player
            player.set_status_callback(self._on_bgm_status)
            player.set_error_callback(self._on_bgm_error)
            player.set_volume(self.slider_bgm_volume.value())
            self.presenter.test_bgm_audio(url)
        else:
            self.lbl_bgm_status.setText("⚠️ Trình phát nhạc chưa sẵn sàng.")
            self.lbl_bgm_status.setStyleSheet("color: #ffcc00;")
            self.stop_test_audio()

    def _on_bgm_status(self, msg: str):
        if self.is_testing_audio:
            self.lbl_bgm_status.setText(msg)
            if "sẵn sàng" in msg.lower() or "đang phát" in msg.lower():
                self.lbl_bgm_status.setStyleSheet("color: #00ff88;")

    def _on_bgm_error(self, err: str):
        self.lbl_bgm_status.setText(f"❌ {err}")
        self.lbl_bgm_status.setStyleSheet("color: #ff5555;")
        self.stop_test_audio()

    def stop_test_audio(self):
        if not self.is_testing_audio:
            return
        self.is_testing_audio = False
        self.btn_test_bgm.setText("▶ Nghe Thử")
        if self.presenter and self.presenter.manage_bgm_uc:
            self.presenter.manage_bgm_uc.stop()

    def _on_bgm_volume_changed(self, val: int):
        self.lbl_bgm_vol_val.setText(f"{val}%")
        if self.presenter:
            self.presenter.set_bgm_volume(val, persist=False)

    def _on_bgm_volume_released(self):
        val = self.slider_bgm_volume.value()
        if self.presenter:
            self.presenter.persist_bgm_volume(val)

    def reject(self):
        self.stop_test_audio()
        super().reject()

    def save_data(self):
        if self.is_testing_audio:
            self.stop_test_audio()

        folder = self.txt_folder.text()
        if folder != "Chưa chọn thư mục" and os.path.exists(folder):
            self.settings.image_folder = folder
            self.settings.interval_ms = self.spn_interval.value() * 1000
            url_str = self.txt_youtube_url.text().strip()
            new_source = self.cmb_bgm_source.currentData() or "youtube"
            source_changed = (url_str != self.initial_youtube_url) or (new_source != self.initial_bgm_source)

            self.settings.bgm_enabled = bool(url_str)
            self.settings.bgm_source = new_source
            self.settings.bgm_youtube_url = url_str
            self.settings.bgm_volume = self.slider_bgm_volume.value()
            self.settings.bgm_loop = self.chk_bgm_loop.isChecked()
            self.settings.transition_type = self.cmb_effect.currentData() or TransitionType.FADE
            self.settings_repo.save_settings(self.settings)

            if self.presenter:
                self.presenter.settings = self.settings
                if source_changed:
                    # Khi đổi link hoặc nguồn nhạc thì mới dừng nhạc và cập nhật nguồn mới
                    if self.presenter.is_bgm_playing():
                        self.presenter.stop_bgm()
                    self.presenter.update_bgm_config(self.presenter.get_bgm_config())
                else:
                    # Nguồn nhạc không đổi: chỉ cập nhật âm lượng, lặp lại mà không nạp lại nguồn
                    self.presenter.apply_bgm_settings_without_reload(self.presenter.get_bgm_config())

                self.presenter.update_transition_type(self.settings.transition_type)
            self.accept()
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một thư mục ảnh hợp lệ!")

    def open_favorites_window(self):
        dialog = FavoritesWindow(self)
        dialog.exec()

