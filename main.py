import sys
import time
import os
from PyQt6.QtWidgets import QApplication, QDialog
from src.viewer_window import PhotoViewerWindow
from src.splash_screen import CustomSplashScreen
from src.settings_dialog import SettingsDialog
from src.config import load_settings
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # Chuỗi id bất kỳ
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    app = QApplication(sys.argv)

    # Đặt icon cho toàn bộ ứng dụng
    # LƯU Ý: Đảm bảo file app_icon.ico (hoặc .png) nằm đúng ở thư mục dự án
    if os.path.exists("app_icon.ico"):
        from PyQt6.QtGui import QIcon
        app.setWindowIcon(QIcon("app_icon.ico"))
    elif os.path.exists("app_icon.png"):
        from PyQt6.QtGui import QIcon
        app.setWindowIcon(QIcon("app_icon.png"))

    # 1. Loading Screen
    splash = CustomSplashScreen()
    splash.show()
    app.processEvents()

    for i in range(1, 101):
        time.sleep(0.012)
        if i == 30:
            splash.set_progress(i, "Đang nạp cấu hình...")
        elif i == 70:
            splash.set_progress(i, "Tải danh sách tài nguyên...")
        else:
            splash.set_progress(i)
        app.processEvents()

    # 2. Kiểm tra thư mục lần đầu chạy
    settings = load_settings()
    folder = settings.get("image_folder", "")

    if not folder or not os.path.exists(folder):
        splash.hide()
        dialog = SettingsDialog()
        dialog.setWindowTitle("Cấu Hình Thư Mục Lần Đầu Chạy")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)

    # 3. Mở cửa sổ chính
    window = PhotoViewerWindow()
    window.show()
    splash.finish(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()