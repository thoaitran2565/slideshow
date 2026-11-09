from typing import Optional, List, Tuple, Dict, Callable
from src.domain.models import ImageItem, Playlist, ViewerSettings, BgmConfig, ImageTransformState, BgmPlaybackState
from src.application.use_cases import (
    LoadImagesUseCase, NavigatePlaylistUseCase,
    DeleteImageUseCase, ManageFavoritesUseCase, ManageSettingsUseCase,
    ManageBgmUseCase
)
from src.domain.ports import SystemIntegrationPort


class ViewerPresenter:
    """Presenter điều phối luồng dữ liệu và nghiệp vụ giữa Views và Use Cases."""
    def __init__(
        self,
        load_images_uc: LoadImagesUseCase,
        navigate_uc: NavigatePlaylistUseCase,
        delete_image_uc: DeleteImageUseCase,
        manage_favorites_uc: ManageFavoritesUseCase,
        manage_settings_uc: ManageSettingsUseCase,
        system_adapter: SystemIntegrationPort,
        manage_bgm_uc: Optional[ManageBgmUseCase] = None
    ):
        self.load_images_uc = load_images_uc
        self.navigate_uc = navigate_uc
        self.delete_image_uc = delete_image_uc
        self.manage_favorites_uc = manage_favorites_uc
        self.manage_settings_uc = manage_settings_uc
        self.system_adapter = system_adapter
        self.manage_bgm_uc = manage_bgm_uc

        self.playlist: Playlist = Playlist()
        self.settings: ViewerSettings = self.manage_settings_uc.get_settings()

        # Bộ nhớ đệm phiên lưu trữ góc xoay và trạng thái lật ảnh (Non-destructive Session Cache)
        self.transform_cache: Dict[str, ImageTransformState] = {}

    def load_initial_images(self, folder: str, start_file: Optional[str] = None) -> int:
        """Nạp danh sách ảnh ban đầu."""
        self.settings = self.manage_settings_uc.get_settings()
        self.playlist = self.load_images_uc.execute(
            folder_path=folder,
            start_file=start_file,
            favorites=self.settings.favorites
        )
        # Khôi phục trạng thái phát ngẫu nhiên từ cấu hình
        self.playlist.is_random = self.settings.is_random
        return self.playlist.total_count

    def reload_images(self, folder: Optional[str] = None) -> int:
        """Nạp lại danh sách ảnh từ thư mục hiện tại."""
        target_folder = folder or self.settings.image_folder
        return self.load_initial_images(target_folder)

    def get_current_item(self) -> Optional[ImageItem]:
        return self.playlist.current_item

    def get_current_path(self) -> Optional[str]:
        item = self.playlist.current_item
        return item.path if item else None

    def get_info_text(self) -> str:
        return self.playlist.get_info_text()

    def next_image(self) -> Optional[ImageItem]:
        return self.navigate_uc.next_image(self.playlist)

    def prev_image(self) -> Optional[ImageItem]:
        return self.navigate_uc.prev_image(self.playlist)

    def set_random(self, is_random: bool) -> None:
        self.navigate_uc.set_random(self.playlist, is_random)
        self.manage_settings_uc.update_random_state(is_random)
        self.settings.is_random = is_random

    def set_control_panel_visibility(self, show_panel: bool) -> None:
        self.manage_settings_uc.update_panel_visibility(show_panel)
        self.settings.show_control_panel = show_panel

    def is_random(self) -> bool:
        return self.playlist.is_random

    def is_current_favorite(self) -> bool:
        curr = self.playlist.current_item
        return curr.is_favorite if curr else False

    def toggle_favorite(self, file_path: Optional[str] = None) -> bool:
        target_path = file_path or self.get_current_path()
        if not target_path:
            return False
        new_state = self.manage_favorites_uc.toggle_favorite(target_path, self.playlist)
        self.settings = self.manage_settings_uc.get_settings()
        return new_state

    def delete_current_image(self) -> Tuple[bool, str, Optional[ImageItem]]:
        return self.delete_image_uc.execute(self.playlist)

    def update_interval(self, seconds: int) -> int:
        interval_ms = self.manage_settings_uc.update_interval(seconds)
        self.settings.interval_ms = interval_ms
        return interval_ms

    def update_bg_color(self, hex_color: str) -> None:
        self.manage_settings_uc.update_bg_color(hex_color)
        self.settings.bg_color = hex_color

    def save_window_state(self, geometry: List[int], is_maximized: bool, is_fullscreen: bool) -> None:
        self.manage_settings_uc.update_window_state(geometry, is_maximized, is_fullscreen)

    def reveal_in_explorer(self, file_path: Optional[str] = None) -> None:
        target = file_path or self.get_current_path()
        if target:
            self.system_adapter.reveal_in_explorer(target)

    # --- Quản lý Nhạc Nền (BGM) ---
    def play_bgm(self) -> None:
        if self.manage_bgm_uc:
            self.manage_bgm_uc.play()

    def pause_bgm(self) -> None:
        if self.manage_bgm_uc:
            self.manage_bgm_uc.pause()

    def stop_bgm(self) -> None:
        if self.manage_bgm_uc:
            self.manage_bgm_uc.stop()

    def set_bgm_state_callback(self, callback: Callable[[BgmPlaybackState, Optional[str]], None]) -> None:
        if self.manage_bgm_uc and hasattr(self.manage_bgm_uc.music_player, 'set_state_callback'):
            self.manage_bgm_uc.music_player.set_state_callback(callback)

    def is_bgm_playing(self) -> bool:
        if self.manage_bgm_uc:
            return self.manage_bgm_uc.is_playing()
        return False

    def is_bgm_ready(self) -> bool:
        """Kiểm tra xem người dùng đã cấu hình URL nhạc hợp lệ chưa."""
        return bool(self.settings.bgm_youtube_url and self.settings.bgm_youtube_url.strip())

    def toggle_bgm(self) -> bool:
        """Bật / Tắt nhanh nhạc nền."""
        if not self.manage_bgm_uc:
            return False
        config = self.manage_bgm_uc.get_bgm_config()
        config.enabled = not config.enabled
        self.manage_bgm_uc.update_bgm_config(config)
        self.settings.bgm_enabled = config.enabled
        return config.enabled

    def get_bgm_config(self) -> BgmConfig:
        if self.manage_bgm_uc:
            return self.manage_bgm_uc.get_bgm_config()
        return BgmConfig()

    def update_bgm_config(self, config: BgmConfig) -> None:
        if self.manage_bgm_uc:
            self.manage_bgm_uc.update_bgm_config(config)
            self.settings = self.manage_settings_uc.get_settings()

    def apply_bgm_settings_without_reload(self, config: BgmConfig) -> None:
        if self.manage_bgm_uc:
            self.manage_bgm_uc.apply_settings_without_reload(config)
            self.settings = self.manage_settings_uc.get_settings()

    def test_bgm_audio(self, url: str) -> None:
        if self.manage_bgm_uc:
            self.manage_bgm_uc.test_audio(url)

    def set_bgm_volume(self, volume: int, persist: bool = False) -> None:
        self.settings.bgm_volume = volume
        if self.manage_bgm_uc:
            self.manage_bgm_uc.set_volume(volume, persist=persist)

    def persist_bgm_volume(self, volume: int) -> None:
        self.settings.bgm_volume = volume
        if self.manage_bgm_uc:
            self.manage_bgm_uc.persist_volume(volume)

    # --- Quản lý Biến Đổi Hình Học Ảnh (Rotation & Flip) ---
    def get_current_transform(self) -> ImageTransformState:
        curr_path = self.get_current_path() or "__current__"
        return self.transform_cache.setdefault(curr_path, ImageTransformState())

    def rotate_current(self, clockwise: bool = True) -> ImageTransformState:
        transform = self.get_current_transform()
        if clockwise:
            transform.rotate_cw()
        else:
            transform.rotate_ccw()
        return transform

    def flip_current_h(self) -> ImageTransformState:
        transform = self.get_current_transform()
        transform.toggle_flip_h()
        return transform

    def flip_current_v(self) -> ImageTransformState:
        transform = self.get_current_transform()
        transform.toggle_flip_v()
        return transform

    def reset_current_transform(self) -> ImageTransformState:
        transform = self.get_current_transform()
        transform.reset()
        return transform

    # --- Quản lý Hiệu Ứng Chuyển Cảnh ---
    def get_transition_type(self) -> str:
        return self.settings.transition_type

    def update_transition_type(self, transition_type: str) -> None:
        self.settings.transition_type = transition_type
        self.manage_settings_uc.update_settings(self.settings)


