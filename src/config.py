import json
import os

SETTINGS_FILE = "settings.json"
SUPPORTED_EXTENSIONS = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.webp')

DEFAULT_SETTINGS = {
    "interval_ms": 3000,
    "bg_color": "#000000",
    "favorites": []  # <--- THÊM DÒNG NÀY ĐỂ LƯU DANH SÁCH YÊU THÍCH
}

def load_settings():
    """Tải cài đặt từ file JSON, nếu không có sẽ dùng cài đặt mặc định."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Lưu cài đặt vào file JSON."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Lỗi lưu cấu hình: {e}")