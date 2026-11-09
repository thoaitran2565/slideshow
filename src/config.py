"""
Shim tương thích ngược cho cấu hình:
Chuyển tiếp các lời gọi sang JsonSettingsRepository trong tầng Infrastructure.
"""
from typing import Dict, Any
from src.domain.models import ViewerSettings, SUPPORTED_EXTENSIONS
from src.infrastructure.json_settings_repo import JsonSettingsRepository

_repo = JsonSettingsRepository()

DEFAULT_SETTINGS = {
    "interval_ms": 3000,
    "bg_color": "#000000",
    "favorites": []
}


def load_settings() -> Dict[str, Any]:
    """Tải cài đặt dạng dictionary tương thích mã nguồn cũ."""
    settings = _repo.load_settings()
    return {
        "image_folder": settings.image_folder,
        "interval_ms": settings.interval_ms,
        "bg_color": settings.bg_color,
        "favorites": settings.favorites,
        "is_maximized": settings.is_maximized,
        "is_fullscreen": settings.is_fullscreen,
        "window_geometry": settings.window_geometry,
        "is_random": settings.is_random,
        "show_control_panel": settings.show_control_panel
    }


def save_settings(data: Dict[str, Any]) -> None:
    """Lưu cài đặt từ dictionary tương thích mã nguồn cũ."""
    settings = ViewerSettings(
        image_folder=data.get("image_folder", ""),
        interval_ms=data.get("interval_ms", 3000),
        bg_color=data.get("bg_color", "#000000"),
        favorites=data.get("favorites", []),
        is_maximized=data.get("is_maximized", False),
        is_fullscreen=data.get("is_fullscreen", False),
        window_geometry=data.get("window_geometry", [100, 100, 1050, 720]),
        is_random=data.get("is_random", False),
        show_control_panel=data.get("show_control_panel", True)
    )
    _repo.save_settings(settings)
