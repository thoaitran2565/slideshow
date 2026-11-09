import json
import os
from typing import Dict, Any
from src.domain.models import ViewerSettings
from src.domain.ports import SettingsRepositoryPort
from src.infrastructure.path_utils import get_base_dir

SETTINGS_FILENAME = "settings.json"


class JsonSettingsRepository(SettingsRepositoryPort):
    """Đọc và ghi tệp cấu hình settings.json với cơ chế fallback an toàn."""
    def __init__(self, filename: str = SETTINGS_FILENAME):
        self.filename = filename

    def _get_file_path(self) -> str:
        # Tệp settings.json luôn nằm cạnh thư mục chạy ứng dụng
        return os.path.join(get_base_dir(), self.filename)

    def load_settings(self) -> ViewerSettings:
        file_path = self._get_file_path()
        if not os.path.exists(file_path):
            default_settings = ViewerSettings()
            self.save_settings(default_settings)
            return default_settings

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)

            raw_url = data.get("bgm_youtube_url", "")
            has_url = bool(raw_url and raw_url.strip())
            # Nếu có URL nhạc thì tự động kích hoạt tính năng nhạc (tương thích loại bỏ checkbox)
            bgm_enabled = has_url if raw_url else data.get("bgm_enabled", False)

            return ViewerSettings(
                image_folder=data.get("image_folder", ""),
                interval_ms=max(1000, data.get("interval_ms", 3000)),
                bg_color=data.get("bg_color", "#000000"),
                favorites=data.get("favorites", []),
                is_maximized=data.get("is_maximized", False),
                is_fullscreen=data.get("is_fullscreen", False),
                window_geometry=data.get("window_geometry", [100, 100, 1050, 720]),
                is_random=data.get("is_random", False),
                show_control_panel=data.get("show_control_panel", True),
                bgm_enabled=bgm_enabled,
                bgm_source=data.get("bgm_source", "youtube"),
                bgm_youtube_url=raw_url,
                bgm_volume=data.get("bgm_volume", 70),
                bgm_loop=data.get("bgm_loop", True),
                transition_type=data.get("transition_type", "fade")
            )
        except Exception as e:
            print(f"[Warning] Không thể nạp {file_path} ({e}), khôi phục cài đặt mặc định.")
            return ViewerSettings()

    def save_settings(self, settings: ViewerSettings) -> None:
        file_path = self._get_file_path()
        has_url = bool(settings.bgm_youtube_url and settings.bgm_youtube_url.strip())
        bgm_enabled = has_url if settings.bgm_youtube_url else settings.bgm_enabled
        data = {
            "image_folder": settings.image_folder,
            "interval_ms": settings.interval_ms,
            "bg_color": settings.bg_color,
            "favorites": settings.favorites,
            "is_maximized": settings.is_maximized,
            "is_fullscreen": settings.is_fullscreen,
            "window_geometry": settings.window_geometry,
            "is_random": settings.is_random,
            "show_control_panel": settings.show_control_panel,
            "bgm_enabled": bgm_enabled,
            "bgm_source": settings.bgm_source,
            "bgm_youtube_url": settings.bgm_youtube_url,
            "bgm_volume": settings.bgm_volume,
            "bgm_loop": settings.bgm_loop,
            "transition_type": settings.transition_type
        }
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[Error] Lỗi khi lưu cấu hình vào {file_path}: {e}")

