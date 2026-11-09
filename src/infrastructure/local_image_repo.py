import os
import glob
from typing import List, Tuple
from send2trash import send2trash
from src.domain.ports import ImageRepositoryPort


class LocalImageRepository(ImageRepositoryPort):
    """Thao tác quét và xóa tệp ảnh trên ổ đĩa cục bộ."""
    def scan_images(self, folder: str, supported_extensions: tuple) -> List[str]:
        if not folder or not os.path.exists(folder):
            return []

        abs_folder = os.path.abspath(folder)
        paths: List[str] = []

        for ext in supported_extensions:
            # Quét cả chữ thường và chữ hoa (ví dụ: *.jpg và *.JPG)
            pattern_lower = os.path.join(abs_folder, f"*{ext}")
            pattern_upper = os.path.join(abs_folder, f"*{ext.upper()}")
            paths.extend(glob.glob(pattern_lower))
            paths.extend(glob.glob(pattern_upper))

        # Loại bỏ trùng lặp và chuẩn hóa đường dẫn
        unique_paths = list(set(os.path.normpath(p) for p in paths))
        return unique_paths

    def delete_image(self, path: str) -> Tuple[bool, str]:
        if not path or not os.path.exists(path):
            return False, f"Tệp không tồn tại: {path}"

        try:
            send2trash(os.path.normpath(path))
            return True, f"Đã chuyển tệp vào Recycle Bin: {os.path.basename(path)}"
        except Exception as e:
            return False, f"Không thể xóa tệp ({e})"

