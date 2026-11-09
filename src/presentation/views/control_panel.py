from typing import Optional
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QGraphicsDropShadowEffect, QSlider
)


class BackdropOverlay(QWidget):
    """Lớp phủ trong suốt bao trùm toàn bộ cửa sổ để chặn click xuyên thấu khi popup mở."""
    dismissed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")
        self.hide()

    def mousePressEvent(self, event):
        event.accept()
        self.dismissed.emit()


class QuickVolumePopup(QWidget):
    """Cửa sổ popup nổi điều chỉnh âm lượng nhanh Dark Theme."""
    volume_changed = pyqtSignal(int)
    volume_saved = pyqtSignal(int)
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        container = QWidget(self)
        container.setObjectName("VolumePopupContainer")
        container.setStyleSheet("""
            QWidget#VolumePopupContainer {
                background-color: rgba(24, 24, 24, 250);
                border: 2px solid #00adb5;
                border-radius: 12px;
            }
            QLabel {
                color: #FFFFFF;
                font-weight: bold;
                font-size: 12px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #444;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #00adb5;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                width: 14px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 7px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 200))
        container.setGraphicsEffect(shadow)

        h_layout = QHBoxLayout(container)
        h_layout.setContentsMargins(12, 10, 12, 10)
        h_layout.setSpacing(8)

        self.lbl_icon = QLabel("🔊")
        h_layout.addWidget(self.lbl_icon)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setFixedWidth(130)
        self.slider.valueChanged.connect(self._on_value_changed)
        self.slider.sliderReleased.connect(self._on_slider_released)
        h_layout.addWidget(self.slider)

        self.lbl_val = QLabel("50%")
        self.lbl_val.setFixedWidth(38)
        self.lbl_val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        h_layout.addWidget(self.lbl_val)

        layout.addWidget(container)

    def set_volume(self, volume: int):
        self.slider.blockSignals(True)
        self.slider.setValue(volume)
        self.lbl_val.setText(f"{volume}%")
        self.lbl_icon.setText("🔇" if volume == 0 else "🔊")
        self.slider.blockSignals(False)

    def _on_value_changed(self, val: int):
        self.lbl_val.setText(f"{val}%")
        self.lbl_icon.setText("🔇" if val == 0 else "🔊")
        self.volume_changed.emit(val)

    def _on_slider_released(self):
        self.volume_saved.emit(self.slider.value())

    def show_above(self, target_widget: QWidget):
        self.adjustSize()
        target_global = target_widget.mapToGlobal(QPoint(0, 0))
        x = target_global.x() + (target_widget.width() - self.width()) // 2
        y = target_global.y() - self.height() - 8
        self.move(x, y)
        self.show()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.closed.emit()


class ControlPanel(QWidget):
    """Bảng điều khiển nổi Dark Theme với độ tương phản cao và hiệu ứng đổ bóng."""
    interval_changed = pyqtSignal(int)
    bgm_volume_changed = pyqtSignal(int)
    bgm_volume_saved = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interval_seconds = 3
        self.volume_popup = None
        self.current_bgm_volume = 50
        self.init_ui()

    def init_ui(self):
        # Thiết kế Floating Card nền đen sâu #121212 với viền sáng rõ ràng
        self.setStyleSheet("""
            QWidget#ControlPanelRoot {
                background-color: rgba(18, 18, 18, 245);
                border: 2px solid rgba(255, 255, 255, 120);
                border-radius: 20px;
            }
            QPushButton {
                background-color: rgba(35, 35, 35, 235);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 80);
                padding: 6px 14px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #00adb5;
                color: #000000;
                border-color: #00adb5;
            }
            QPushButton:checked {
                background-color: #0078D4;
                color: #FFFFFF;
                border-color: #0086F0;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#btnStep {
                background-color: rgba(45, 45, 45, 235);
                padding: 4px 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.setObjectName("ControlPanelRoot")

        # Hiệu ứng đổ bóng ngoài (Drop Shadow) giúp panel nổi bật trên mọi nền ảnh sáng
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 210))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(10)

        # Các nút thao tác chính
        self.btn_play_pause = QPushButton("⏸ Pause")
        self.btn_random = QPushButton("🔀 Random")
        self.btn_random.setCheckable(True)
        self.btn_rotate = QPushButton("🔄 Xoay")
        self.btn_bgm = QPushButton("🎵 Nhạc")
        self.btn_color = QPushButton("🎨 Nền")

        # Bộ chỉnh thời gian (+ / -)
        self.lbl_time_title = QLabel("Tốc độ:")
        self.btn_minus = QPushButton("−")
        self.btn_minus.setObjectName("btnStep")
        self.lbl_interval_val = QLabel("3s")
        self.lbl_interval_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_plus = QPushButton("+")
        self.btn_plus.setObjectName("btnStep")

        self.btn_hide = QPushButton("👁️ Ẩn")

        # Gắn vào Layout
        layout.addWidget(self.btn_play_pause)
        layout.addWidget(self.btn_random)
        layout.addWidget(self.btn_rotate)
        layout.addWidget(self.btn_bgm)
        layout.addWidget(self.btn_color)

        # Cụm thời gian
        layout.addWidget(self.lbl_time_title)
        layout.addWidget(self.btn_minus)
        layout.addWidget(self.lbl_interval_val)
        layout.addWidget(self.btn_plus)

        layout.addWidget(self.btn_hide)

        # Kết nối sự kiện nút tăng / giảm thời gian
        self.btn_minus.clicked.connect(self.decrease_interval)
        self.btn_plus.clicked.connect(self.increase_interval)

        # Chuột phải vào nút BGM để mở popup âm lượng nhanh
        self.btn_bgm.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.btn_bgm.customContextMenuRequested.connect(self._show_volume_popup)

    def set_current_bgm_volume(self, volume: int):
        self.current_bgm_volume = volume
        if self.volume_popup:
            self.volume_popup.set_volume(volume)

    def _show_volume_popup(self, pos):
        window = self.window()
        overlay = getattr(window, "backdrop_overlay", None)

        if not self.volume_popup:
            self.volume_popup = QuickVolumePopup(window)
            self.volume_popup.volume_changed.connect(self.bgm_volume_changed.emit)
            self.volume_popup.volume_saved.connect(self.bgm_volume_saved.emit)
            if overlay:
                overlay.dismissed.connect(self.volume_popup.hide)
                self.volume_popup.closed.connect(overlay.hide)

        if overlay:
            overlay.setGeometry(window.rect())
            overlay.show()
            overlay.raise_()

        self.volume_popup.set_volume(self.current_bgm_volume)
        self.volume_popup.show_above(self.btn_bgm)
        self.volume_popup.raise_()

    def set_interval_value(self, seconds: int):
        self.interval_seconds = max(1, seconds)
        self.lbl_interval_val.setText(f"{self.interval_seconds}s")

    def decrease_interval(self):
        if self.interval_seconds > 1:
            self.interval_seconds -= 1
            self.lbl_interval_val.setText(f"{self.interval_seconds}s")
            self.interval_changed.emit(self.interval_seconds)

    def increase_interval(self):
        self.interval_seconds += 1
        self.lbl_interval_val.setText(f"{self.interval_seconds}s")
        self.interval_changed.emit(self.interval_seconds)

    def set_play_state(self, is_playing: bool):
        self.btn_play_pause.setText("⏸ Pause" if is_playing else "▶ Play")

    def set_bgm_loading(self, is_loading: bool, error_msg: Optional[str] = None):
        if is_loading:
            self.btn_bgm.setText("⏳ Đang tải...")
            self.btn_bgm.setToolTip("Đang kết nối luồng nhạc, vui lòng đợi...")
            self.btn_bgm.setEnabled(False)
        else:
            self.btn_bgm.setEnabled(True)
            if error_msg:
                self.btn_bgm.setText("🎵 Bật nhạc")
                self.btn_bgm.setToolTip(f"❌ {error_msg}")

    def set_bgm_state(self, is_enabled: bool, is_playing: bool = False):
        if is_playing:
            self.btn_bgm.setText("🔇 Tắt nhạc")
            self.btn_bgm.setToolTip("Tắt nhạc nền (Chuột phải để chỉnh âm lượng)")
        else:
            self.btn_bgm.setText("🎵 Bật nhạc")
            self.btn_bgm.setToolTip("Bật nhạc nền (Chuột phải để chỉnh âm lượng)")
