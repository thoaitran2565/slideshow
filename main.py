import sys
import time
import os
from PyQt6.QtWidgets import QApplication, QDialog
from src.viewer_window import PhotoViewerWindow
from src.splash_screen import CustomSplashScreen
from src.settings_dialog import SettingsDialog
import winreg as reg
from src.config import load_settings
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # Chuỗi id bất kỳ
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    auto_register_file_association()
    
    app = QApplication(sys.argv)

    # Đặt icon cho toàn bộ ứng dụng
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

    # Xử lý tham số mở file từ "Open with" (nếu có)
    target_file = None
    initial_dir = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path) and os.path.isfile(file_path):
            target_file = file_path
            initial_dir = os.path.dirname(file_path)

    # 2. Kiểm tra thư mục lần đầu chạy (nếu không mở qua Open with và chưa có cấu hình thư mục)
    settings = load_settings()
    folder = initial_dir or settings.get("image_folder", "")

    if not folder or not os.path.exists(folder):
        splash.hide()
        dialog = SettingsDialog()
        dialog.setWindowTitle("Cấu Hình Thư Mục Lần Đầu Chạy")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)
        settings = load_settings()
        folder = settings.get("image_folder", "")

    # 3. Mở cửa sổ chính, truyền thêm start_file và thư mục phù hợp
    window = PhotoViewerWindow(image_dir=folder, start_file=target_file)
    window.show()
    splash.finish(window)

    sys.exit(app.exec())

def auto_register_file_association():
    """Tự động đăng ký Open with vào Windows Registry cho các định dạng ảnh"""
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable  # Đường dẫn file .exe thực tế
    else:
        exe_path = os.path.abspath(sys.argv[0])

    app_name = "WindowsPhotoSlideshow"
    app_verb = "Trình chiếu ảnh cá nhân"
    extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

    try:
        for ext in extensions:
            # 1. Đăng ký đuôi mở rộng
            reg_path_ext = f"Software\\Classes\\{ext}"
            with reg.CreateKey(reg.HKEY_CURRENT_USER, reg_path_ext) as key:
                reg.SetValue(key, "", reg.REG_SZ, f"{app_name}.Assoc")

            # 2. Đăng ký ProgID
            reg_path_progid = f"Software\\Classes\\{app_name}.Assoc"
            with reg.CreateKey(reg.HKEY_CURRENT_USER, reg_path_progid) as key:
                reg.SetValue(key, "", reg.REG_SZ, app_verb)

            # 3. Đăng ký câu lệnh thực thi
            reg_path_cmd = f"Software\\Classes\\{app_name}.Assoc\\shell\\open\\command"
            with reg.CreateKey(reg.HKEY_CURRENT_USER, reg_path_cmd) as key:
                command_str = f'"{exe_path}" "%1"'
                reg.SetValue(key, "", reg.REG_SZ, command_str)
    except Exception as e:
        print(f"Lỗi đăng ký Registry tự động: {e}")

if __name__ == "__main__":
    main()