import os
import sys
import ctypes
import winreg as reg
from src.domain.ports import SystemIntegrationPort


class WindowsSystemAdapter(SystemIntegrationPort):
    """Adapter tích hợp các tính năng đặc thù của hệ điều hành Windows."""

    def register_file_associations(self, exe_path: str) -> None:
        """Tự động đăng ký Open with vào Windows Registry cho các định dạng ảnh."""
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
            print(f"[Warning] Lỗi đăng ký Registry tự động: {e}")

    def set_app_user_model_id(self, app_id: str) -> None:
        """Gán AppUserModelID để Windows Taskbar hiển thị icon ứng dụng chuẩn."""
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception as e:
            print(f"[Warning] Không thể đặt AppUserModelID: {e}")

    def reveal_in_explorer(self, file_path: str) -> None:
        """Mở Windows Explorer và highlight tệp tin."""
        if file_path and os.path.exists(file_path):
            norm_path = os.path.normpath(file_path)
            os.system(f'explorer /select,"{norm_path}"')

