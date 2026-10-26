from PyQt6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QPoint
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

    def move_to_screen_center(self, app, saved_geometry):
        """Định vị splash screen ra đúng màn hình chứa tọa độ ứng dụng lần trước"""
        if saved_geometry and len(saved_geometry) == 4:
            center_x = saved_geometry[0] + saved_geometry[2] // 2
            center_y = saved_geometry[1] + saved_geometry[3] // 2
            
            screen = app.screenAt(QPoint(center_x, center_y))
            if screen:
                screen_geo = screen.geometry()
                splash_x = screen_geo.x() + (screen_geo.width() - self.width()) // 2
                splash_y = screen_geo.y() + (screen_geo.height() - self.height()) // 2
                self.move(splash_x, splash_y)