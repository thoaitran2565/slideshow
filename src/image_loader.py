import os
import glob
import random
import re
from send2trash import send2trash
from src.config import SUPPORTED_EXTENSIONS


class ImageManager:
    def __init__(self, image_dir="images"):
        self.image_dir = image_dir
        self.image_paths = []
        self.current_index = 0
        self.is_random = False
        self.history = []

    def _natural_sort_key(self, s):
        """Hàm hỗ trợ sắp xếp tên file theo kiểu tự nhiên của Windows (ví dụ: 2.jpg đứng trước 10.jpg)"""
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

    def load_images(self, start_file=None):
        abs_path = os.path.abspath(self.image_dir)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        paths = []
        for ext in SUPPORTED_EXTENSIONS:
            paths.extend(glob.glob(os.path.join(abs_path, ext)))
            paths.extend(glob.glob(os.path.join(abs_path, ext.upper())))

        # Sắp xếp danh sách file theo tên tự nhiên (giống hệt cách Explorer sắp xếp mặc định)
        self.image_paths = sorted(list(set(paths)), key=lambda x: self._natural_sort_key(os.path.basename(x)))
        
        # Nếu có file chỉ định mở trực tiếp từ "Open with"
        if start_file:
            norm_start = os.path.normpath(start_file)
            matched_index = -1
            for idx, path in enumerate(self.image_paths):
                if os.path.normpath(path) == norm_start:
                    matched_index = idx
                    break
            
            if matched_index != -1:
                self.current_index = matched_index
            else:
                # Trường hợp file nằm ngoài danh sách quét, chèn thủ công vào để hiển thị
                if os.path.exists(norm_start):
                    self.image_paths.insert(0, norm_start)
                    self.current_index = 0
        elif self.image_paths and self.current_index >= len(self.image_paths):
            self.current_index = 0

        return len(self.image_paths)

    def get_current_path(self):
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            return None
        return self.image_paths[self.current_index]

    def get_info_text(self):
        if not self.image_paths:
            return "Không có ảnh"
        path = self.get_current_path()
        filename = os.path.basename(path) if path else ""
        
        if self.is_random:
            return f"🔀 Random - {filename}"
        return f"{self.current_index + 1} / {len(self.image_paths)} - {filename}"

    def next_index(self):
        if not self.image_paths:
            return
        if self.is_random:
            self.history.append(self.current_index)
            self.current_index = random.randint(0, len(self.image_paths) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.image_paths)

    def prev_index(self):
        if not self.image_paths:
            return
        if self.is_random and self.history:
            self.current_index = self.history.pop()
        else:
            self.current_index = (self.current_index - 1) % len(self.image_paths)

    def delete_current_image(self):
        path = self.get_current_path()
        if not path:
            return False, "Không có ảnh để xóa"

        send2trash(path)
        del self.image_paths[self.current_index]

        if self.image_paths:
            self.current_index %= len(self.image_paths)
        return True, path