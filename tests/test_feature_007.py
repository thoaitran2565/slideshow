import os
import sys
import unittest
from unittest.mock import MagicMock

# Đảm bảo import được các module từ src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.domain.models import ViewerSettings, BgmConfig, BgmPlaybackState
from src.domain.ports import MusicPlayerPort, SettingsRepositoryPort
from src.application.use_cases import ManageBgmUseCase
from src.presentation.presenter import ViewerPresenter
from src.infrastructure.json_settings_repo import JsonSettingsRepository


class MockMusicPlayer(MusicPlayerPort):
    def __init__(self):
        self.current_target = ""
        self.playing = False
        self.volume = 70
        self.loop = True
        self.status_callback = None
        self.error_callback = None
        self.source_set_history = []
        self.play_called_count = 0

    def set_source(self, source_target: str) -> None:
        self.current_target = source_target
        self.source_set_history.append(source_target)
        self.playing = True

    def get_source(self) -> str:
        return self.current_target

    def play(self) -> None:
        self.play_called_count += 1
        if self.current_target:
            self.playing = True

    def pause(self) -> None:
        self.playing = False

    def stop(self) -> None:
        self.playing = False

    def set_volume(self, volume: int) -> None:
        self.volume = volume

    def set_loop(self, loop: bool) -> None:
        self.loop = loop

    def is_playing(self) -> bool:
        return self.playing

    def set_error_callback(self, callback) -> None:
        self.error_callback = callback

    def set_status_callback(self, callback) -> None:
        self.status_callback = callback


class MockSettingsRepo(SettingsRepositoryPort):
    def __init__(self, settings: ViewerSettings):
        self.settings = settings

    def load_settings(self) -> ViewerSettings:
        return self.settings

    def save_settings(self, settings: ViewerSettings) -> None:
        self.settings = settings


class TestFeature007BgmPlayButtonFlow(unittest.TestCase):
    """Bộ kiểm thử cho Feature 007: Khắc phục luồng Bật/Tắt nhạc BGM."""

    def test_t003_is_bgm_ready_when_url_present_and_bgm_enabled_false(self):
        """User Story 1: is_bgm_ready() phải trả về True khi có URL dù bgm_enabled = False."""
        settings = ViewerSettings(
            bgm_enabled=False,  # Cờ cũ bị tắt
            bgm_youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        settings_uc = MagicMock()
        settings_uc.get_settings.return_value = settings

        presenter = ViewerPresenter(
            load_images_uc=MagicMock(),
            navigate_uc=MagicMock(),
            delete_image_uc=MagicMock(),
            manage_favorites_uc=MagicMock(),
            manage_settings_uc=settings_uc,
            system_adapter=MagicMock(),
            manage_bgm_uc=MagicMock()
        )

        # Sau khi fix, is_bgm_ready() chỉ dựa trên URL
        self.assertTrue(
            presenter.is_bgm_ready(),
            "is_bgm_ready() phải trả về True khi có URL hợp lệ kể cả khi bgm_enabled là False"
        )

    def test_t003_is_bgm_ready_when_url_is_empty_or_whitespace(self):
        """User Story 1: is_bgm_ready() phải trả về False khi URL rỗng hoặc chỉ có khoảng trắng."""
        settings_empty = ViewerSettings(bgm_enabled=True, bgm_youtube_url="")
        settings_spaces = ViewerSettings(bgm_enabled=True, bgm_youtube_url="   ")

        settings_uc1 = MagicMock()
        settings_uc1.get_settings.return_value = settings_empty

        presenter1 = ViewerPresenter(
            load_images_uc=MagicMock(),
            navigate_uc=MagicMock(),
            delete_image_uc=MagicMock(),
            manage_favorites_uc=MagicMock(),
            manage_settings_uc=settings_uc1,
            system_adapter=MagicMock(),
            manage_bgm_uc=MagicMock()
        )
        self.assertFalse(presenter1.is_bgm_ready())

        settings_uc2 = MagicMock()
        settings_uc2.get_settings.return_value = settings_spaces

        presenter2 = ViewerPresenter(
            load_images_uc=MagicMock(),
            navigate_uc=MagicMock(),
            delete_image_uc=MagicMock(),
            manage_favorites_uc=MagicMock(),
            manage_settings_uc=settings_uc2,
            system_adapter=MagicMock(),
            manage_bgm_uc=MagicMock()
        )
        self.assertFalse(presenter2.is_bgm_ready())

    def test_t005_toggle_bgm_action_behavior(self):
        """User Story 1: Mô phỏng toggle_bgm_action() không mở settings khi có URL."""
        settings = ViewerSettings(bgm_youtube_url="https://youtube.com/track")
        settings_uc = MagicMock()
        settings_uc.get_settings.return_value = settings
        bgm_uc = MagicMock()
        bgm_uc.is_playing.return_value = False

        presenter = ViewerPresenter(
            load_images_uc=MagicMock(),
            navigate_uc=MagicMock(),
            delete_image_uc=MagicMock(),
            manage_favorites_uc=MagicMock(),
            manage_settings_uc=settings_uc,
            system_adapter=MagicMock(),
            manage_bgm_uc=bgm_uc
        )

        opened_settings = False
        def fake_open_settings():
            nonlocal opened_settings
            opened_settings = True

        # Mô phỏng logic toggle_bgm_action
        if not presenter.is_bgm_ready():
            fake_open_settings()
        else:
            if presenter.is_bgm_playing():
                presenter.stop_bgm()
            else:
                presenter.play_bgm()

        self.assertFalse(opened_settings, "Không được mở Cài đặt khi đã có URL hợp lệ")
        bgm_uc.play.assert_called_once()

    def test_t006_manage_bgm_play_auto_loads_source_when_player_empty(self):
        """User Story 2: ManageBgmUseCase.play() tự động gọi set_source() khi player chưa có nguồn."""
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        settings = ViewerSettings(
            bgm_enabled=False,  # Kể cả cờ này là False
            bgm_youtube_url=test_url
        )
        player = MockMusicPlayer()
        # Ban đầu player chưa có nguồn
        self.assertEqual(player.current_target, "")

        repo = MockSettingsRepo(settings)
        use_case = ManageBgmUseCase(music_player=player, settings_repo=repo)

        # Gọi play() trực tiếp
        use_case.play()

        # Kiểm tra player đã được tự động set_source với đúng URL
        self.assertEqual(player.current_target, test_url)
        self.assertIn(test_url, player.source_set_history)
        self.assertTrue(player.is_playing())

    def test_t006_manage_bgm_play_does_not_reload_if_same_source_already_set(self):
        """User Story 2: Nếu player đã có nguồn trùng khớp thì chỉ gọi play() chứ không set_source() lại."""
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        settings = ViewerSettings(
            bgm_enabled=True,
            bgm_youtube_url=test_url
        )
        player = MockMusicPlayer()
        player.current_target = test_url
        repo = MockSettingsRepo(settings)
        use_case = ManageBgmUseCase(music_player=player, settings_repo=repo)

        use_case.play()

        # Không gọi lại set_source lần thứ hai
        self.assertEqual(len(player.source_set_history), 0)
        self.assertEqual(player.play_called_count, 1)

    def test_t007_qt_music_player_methods(self):
        """Xác nhận QtMusicPlayer có get_source() và không lỗi khi play trên nguồn rỗng."""
        from PyQt6.QtWidgets import QApplication
        from src.infrastructure.bgm.qt_music_player import QtMusicPlayer

        app = QApplication.instance() or QApplication([])
        player = QtMusicPlayer()
        self.assertEqual(player.get_source(), "")
        # Gọi play khi current_target rỗng không làm crash và không chuyển sang PLAYING giả
        player.play()
        self.assertEqual(player.playback_state, BgmPlaybackState.STOPPED)

    def test_t002_json_settings_repo_syncs_bgm_enabled(self):
        """Foundational: JsonSettingsRepository tự động đồng bộ cờ bgm_enabled."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_file = os.path.join(tmp_dir, "test_settings.json")
            repo = JsonSettingsRepository(filename=temp_file)
            repo._get_file_path = lambda: temp_file

            # Cấu hình có URL nhưng bgm_enabled = False
            settings = ViewerSettings(
                bgm_enabled=False,
                bgm_youtube_url="https://youtube.com/song"
            )
            repo.save_settings(settings)

            loaded = repo.load_settings()
            self.assertTrue(loaded.bgm_enabled, "bgm_enabled phải được đồng bộ thành True khi có URL hợp lệ")


if __name__ == "__main__":
    unittest.main()
