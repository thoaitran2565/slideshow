import os
import sys


def get_base_dir() -> str:
    """
    Trả về thư mục gốc làm việc của ứng dụng:
    - Khi chạy bằng PyInstaller (--onefile hoặc --onedir): là thư mục chứa file .exe thực tế
    - Khi chạy qua mã nguồn python: là thư mục gốc của repository
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def get_resource_path(relative_path: str) -> str:
    """
    Tìm đường dẫn tài nguyên tĩnh:
    - Ưu tiên tìm trong thư mục tạm PyInstaller (_MEIPASS nếu có)
    - Sau đó tìm theo thư mục gốc ứng dụng
    """
    if hasattr(sys, '_MEIPASS'):
        bundle_path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(bundle_path):
            return bundle_path

    base_dir = get_base_dir()
    local_path = os.path.join(base_dir, relative_path)
    if os.path.exists(local_path):
        return local_path

    # Thử tìm trực tiếp theo current working directory
    if os.path.exists(relative_path):
        return os.path.abspath(relative_path)

    return local_path

