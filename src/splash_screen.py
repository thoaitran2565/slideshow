from PyQt6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QFont


class CustomSplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(480, 280)
        pixmap.fill(QColor(22, 22, 22))
        super().__init__(pixmap)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 35, 30, 30)

        title = QLabel("PHOTO SLIDESHOW")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #00adb5;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Đang khởi động tài nguyên...")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #aaaaaa;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addStretch()

        self.lbl_status = QLabel("Đang nạp hệ thống...")
        self.lbl_status.setStyleSheet("color: #ffffff; font-size: 11px;")
        layout.addWidget(self.lbl_status)

        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #333333;
                height: 6px;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #00adb5;
                border-radius: 3px;
            }
        """)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

    def set_progress(self, value, message=""):
        self.progress.setValue(value)
        if message:
            self.lbl_status.setText(message)