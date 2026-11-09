import os
from typing import Optional, List, Tuple
from src.domain.models import ImageItem, Playlist, ViewerSettings, BgmConfig, SUPPORTED_EXTENSIONS
from src.domain.ports import ImageRepositoryPort, SettingsRepositoryPort, MusicPlayerPort
from src.application.sorting import natural_sort_key


class LoadImagesUseCase:
    """Nạp danh sách ảnh từ thư mục và khởi tạo Playlist với Natural Sort."""
    def __init__(self, image_repo: ImageRepositoryPort):
        self.image_repo = image_repo

    def execute(self, folder_path: str, start_file: Optional[str] = None, favorites: Optional[List[str]] = None) -> Playlist:
        fav_set = set(os.path.normpath(f) for f in (favorites or []))
        raw_paths = self.image_repo.scan_images(folder_path, SUPPORTED_EXTENSIONS)

        # Sắp xếp tự nhiên theo tên tệp (như Windows Explorer)
        sorted_paths = sorted(list(set(raw_paths)), key=lambda p: natural_sort_key(os.path.basename(p)))

        items: List[ImageItem] = []
        for p in sorted_paths:
            norm_p = os.path.normpath(p)
            items.append(ImageItem(
                path=norm_p,
                filename=os.path.basename(norm_p),
                is_favorite=(norm_p in fav_set)
            ))

        target_index = 0

        # Nếu có start_file (từ Open With)
        if start_file:
            norm_start = os.path.normpath(start_file)
            matched_index = -1
            for idx, item in enumerate(items):
                if item.path == norm_start:
                    matched_index = idx
                    break

            if matched_index != -1:
                target_index = matched_index
            else:
                # Nếu start_file hợp lệ nhưng nằm ngoài thư mục quét, chèn vào đầu
                if os.path.exists(norm_start):
                    start_item = ImageItem(
                        path=norm_start,
                        filename=os.path.basename(norm_start),
                        is_favorite=(norm_start in fav_set)
                    )
                    items.insert(0, start_item)
                    target_index = 0

        return Playlist(items=items, current_index=target_index)


class NavigatePlaylistUseCase:
    """Xử lý chuyển ảnh tới / lui tuần tự hoặc ngẫu nhiên."""
    @staticmethod
    def next_image(playlist: Playlist) -> Optional[ImageItem]:
        return playlist.next()

    @staticmethod
    def prev_image(playlist: Playlist) -> Optional[ImageItem]:
        return playlist.prev()

    @staticmethod
    def set_random(playlist: Playlist, is_random: bool) -> None:
        playlist.is_random = is_random


class DeleteImageUseCase:
    """Điều phối việc xóa ảnh vào Recycle Bin và cập nhật Playlist."""
    def __init__(self, image_repo: ImageRepositoryPort):
        self.image_repo = image_repo

    def execute(self, playlist: Playlist) -> Tuple[bool, str, Optional[ImageItem]]:
        curr = playlist.current_item
        if not curr:
            return False, "Không có ảnh để xóa", None

        success, message = self.image_repo.delete_image(curr.path)
        if success:
            next_item = playlist.remove_current()
            return True, message, next_item
        return False, message, curr


class ManageFavoritesUseCase:
    """Quản lý danh sách ảnh yêu thích."""
    def __init__(self, settings_repo: SettingsRepositoryPort):
        self.settings_repo = settings_repo

    def toggle_favorite(self, file_path: str, playlist: Optional[Playlist] = None) -> bool:
        settings = self.settings_repo.load_settings()
        norm_path = os.path.normpath(file_path)

        favorites = [os.path.normpath(f) for f in settings.favorites]
        is_fav = norm_path in favorites

        if is_fav:
            favorites.remove(norm_path)
            new_state = False
        else:
            favorites.append(norm_path)
            new_state = True

        settings.favorites = favorites
        self.settings_repo.save_settings(settings)

        # Cập nhật trạng thái trong playlist nếu được cung cấp
        if playlist:
            for idx, item in enumerate(playlist.items):
                if item.path == norm_path:
                    playlist.items[idx] = ImageItem(
                        path=item.path,
                        filename=item.filename,
                        is_favorite=new_state
                    )

        return new_state

    def is_favorite(self, file_path: str) -> bool:
        settings = self.settings_repo.load_settings()
        norm_path = os.path.normpath(file_path)
        return norm_path in [os.path.normpath(f) for f in settings.favorites]


class ManageSettingsUseCase:
    """Tải và lưu trữ cấu hình người dùng."""
    def __init__(self, settings_repo: SettingsRepositoryPort):
        self.settings_repo = settings_repo

    def get_settings(self) -> ViewerSettings:
        return self.settings_repo.load_settings()

    def update_settings(self, settings: ViewerSettings) -> None:
        self.settings_repo.save_settings(settings)

    def update_interval(self, seconds: int) -> int:
        settings = self.settings_repo.load_settings()
        settings.interval_ms = max(1000, seconds * 1000)
        self.settings_repo.save_settings(settings)
        return settings.interval_ms

    def update_bg_color(self, hex_color: str) -> None:
        settings = self.settings_repo.load_settings()
        settings.bg_color = hex_color
        self.settings_repo.save_settings(settings)

    def update_window_state(self, geometry: List[int], is_maximized: bool, is_fullscreen: bool) -> None:
        settings = self.settings_repo.load_settings()
        settings.window_geometry = geometry
        settings.is_maximized = is_maximized
        settings.is_fullscreen = is_fullscreen
        self.settings_repo.save_settings(settings)

    def update_random_state(self, is_random: bool) -> None:
        settings = self.settings_repo.load_settings()
        settings.is_random = is_random
        self.settings_repo.save_settings(settings)

    def update_panel_visibility(self, show_panel: bool) -> None:
        settings = self.settings_repo.load_settings()
        settings.show_control_panel = show_panel
        self.settings_repo.save_settings(settings)


class ManageBgmUseCase:
    """Điều phối logic nghiệp vụ nhạc nền (BGM)."""
    def __init__(self, music_player: MusicPlayerPort, settings_repo: SettingsRepositoryPort):
        self.music_player = music_player
        self.settings_repo = settings_repo

    def get_bgm_config(self) -> BgmConfig:
        settings = self.settings_repo.load_settings()
        return BgmConfig(
            enabled=settings.bgm_enabled,
            source=settings.bgm_source,
            youtube_url=settings.bgm_youtube_url,
            volume=settings.bgm_volume,
            loop=settings.bgm_loop
        )

    def update_bgm_config(self, config: BgmConfig) -> None:
        settings = self.settings_repo.load_settings()
        settings.bgm_enabled = config.enabled
        settings.bgm_source = config.source
        settings.bgm_youtube_url = config.youtube_url
        settings.bgm_volume = config.volume
        settings.bgm_loop = config.loop
        self.settings_repo.save_settings(settings)

        self.music_player.set_volume(config.volume)
        self.music_player.set_loop(config.loop)
        if config.enabled and config.youtube_url:
            self.music_player.set_source(config.youtube_url)
        else:
            self.music_player.stop()

    def apply_settings_without_reload(self, config: BgmConfig) -> None:
        """Cập nhật cấu hình BGM (âm lượng, lặp lại) mà không nạp lại nguồn phát."""
        settings = self.settings_repo.load_settings()
        settings.bgm_enabled = config.enabled
        settings.bgm_source = config.source
        settings.bgm_youtube_url = config.youtube_url
        settings.bgm_volume = config.volume
        settings.bgm_loop = config.loop
        self.settings_repo.save_settings(settings)

        self.music_player.set_volume(config.volume)
        self.music_player.set_loop(config.loop)

    def play(self) -> None:
        config = self.get_bgm_config()
        url = (config.youtube_url or "").strip()
        if not url:
            return

        # Luôn đảm bảo đồng bộ âm lượng từ cấu hình xuống player trước khi phát
        self.music_player.set_volume(config.volume)

        current_source = ""
        if hasattr(self.music_player, "get_source"):
            current_source = self.music_player.get_source()
        elif hasattr(self.music_player, "current_target"):
            current_source = getattr(self.music_player, "current_target", "")

        # Nếu player chưa nạp nguồn hoặc nguồn khác với URL cấu hình -> tự động nạp nguồn
        if not current_source or current_source != url:
            self.music_player.set_source(url)
        else:
            self.music_player.play()

    def pause(self) -> None:
        self.music_player.pause()

    def stop(self) -> None:
        self.music_player.stop()

    def is_playing(self) -> bool:
        return self.music_player.is_playing()

    def set_volume(self, volume: int, persist: bool = True) -> None:
        self.music_player.set_volume(volume)
        if persist:
            self.persist_volume(volume)

    def persist_volume(self, volume: int) -> None:
        settings = self.settings_repo.load_settings()
        settings.bgm_volume = volume
        self.settings_repo.save_settings(settings)

    def test_audio(self, url: str) -> None:
        """Kiểm tra nghe thử một URL nhạc."""
        self.music_player.stop()
        self.music_player.set_source(url)
        self.music_player.play()


