from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel


class ControlPanel(QWidget):
    # Khai báo Signal điều chỉnh thời gian
    interval_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interval_seconds = 3
        self.init_ui()

    def init_ui(self):
        # Phong cách Dark Tương Phản Cao (Nền đặc hơn, viền & chữ rõ hơn)
        self.setStyleSheet("""
            QWidget#ControlPanelRoot {
                background-color: rgba(15, 15, 15, 245);  /* Nền tối đậm gần như đặc */
                border: 2px solid rgba(255, 255, 255, 100); /* Viền nét và rõ hơn */
                border-radius: 20px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 60);
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
                padding: 4px 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.setObjectName("ControlPanelRoot")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(10)

        # Các nút thao tác chính
        self.btn_play_pause = QPushButton("⏸ Pause")
        self.btn_random = QPushButton("🔀 Random")
        self.btn_random.setCheckable(True)
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