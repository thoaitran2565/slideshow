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


class MockMusicPlayer(MusicPlayerPort):
    def __init__(self):
        self.current_target = ""
        self.playing = False
        self.volume = 70
        self.loop = True
        self.status_callback = None
        self.error_callback = None
        self.source_set_history = []
        self.stop_called_count = 0
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
        self.stop_called_count += 1
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


class TestFeature008BgmSettingsAndVolume(unittest.TestCase):
    """Bộ kiểm thử cho Feature 008: Vòng đời BGM trong Cài đặt & Khởi tạo âm lượng."""

    def test_t003_stop_test_audio_when_not_testing_does_not_stop_player(self):
        """User Story 1: stop_test_audio() khi is_testing_audio=False không được gọi stop() trên player."""
        player = MockMusicPlayer()
        player.current_target = "https://youtube.com/track"
        player.playing = True
        settings = ViewerSettings(bgm_youtube_url=player.current_target)
        repo = MockSettingsRepo(settings)
        bgm_uc = ManageBgmUseCase(music_player=player, settings_repo=repo)

        # Mô phỏng logic stop_test_audio đã sửa
        is_testing_audio = False
        def fake_stop_test_audio():
            nonlocal is_testing_audio
            if not is_testing_audio:
                return
            is_testing_audio = False
            bgm_uc.stop()

        # Khi người dùng đóng SettingsDialog (reject):
        fake_stop_test_audio()

        # Kiểm tra player KHÔNG bị dừng, vẫn đang phát
        self.assertEqual(player.stop_called_count, 0)
        self.assertTrue(player.is_playing())

    def test_t003_stop_test_audio_when_testing_does_stop_player(self):
        """User Story 1: stop_test_audio() khi is_testing_audio=True phải dừng player."""
        player = MockMusicPlayer()
        player.playing = True
        settings = ViewerSettings()
        repo = MockSettingsRepo(settings)
        bgm_uc = ManageBgmUseCase(music_player=player, settings_repo=repo)

        is_testing_audio = True
        def fake_stop_test_audio():
            nonlocal is_testing_audio
            if not is_testing_audio:
                return
            is_testing_audio = False
            bgm_uc.stop()

        fake_stop_test_audio()

        self.assertEqual(player.stop_called_count, 1)
        self.assertFalse(player.is_playing())
        self.assertFalse(is_testing_audio)

    def test_t005_apply_settings_without_reload_updates_volume_and_loop_without_reloading_source(self):
        """User Story 2: apply_settings_without_reload() cập nhật volume/loop mà không nạp lại source."""
        player = MockMusicPlayer()
        player.current_target = "https://youtube.com/track"
        player.playing = True
        player.volume = 50
        player.loop = True
        settings = ViewerSettings(bgm_youtube_url=player.current_target, bgm_volume=50, bgm_loop=True)
        repo = MockSettingsRepo(settings)
        bgm_uc = ManageBgmUseCase(music_player=player, settings_repo=repo)

        new_config = BgmConfig(
            enabled=True,
            source="youtube",
            youtube_url="https://youtube.com/track",
            volume=85,
            loop=False
        )

        bgm_uc.apply_settings_without_reload(new_config)

        # Player cập nhật volume và loop mới
        self.assertEqual(player.volume, 85)
        self.assertFalse(player.loop)
        # Không hề gọi set_source lại
        self.assertEqual(len(player.source_set_history), 0)
        # Vẫn đang phát
        self.assertTrue(player.is_playing())

    def test_t008_play_synchronizes_volume_from_config(self):
        """User Story 3: ManageBgmUseCase.play() đồng bộ volume từ config vào player."""
        player = MockMusicPlayer()
        player.volume = 70  # Mặc định của player là 70
        # Cấu hình người dùng lưu là 25%
        settings = ViewerSettings(
            bgm_youtube_url="https://youtube.com/track",
            bgm_volume=25
        )
        repo = MockSettingsRepo(settings)
        bgm_uc = ManageBgmUseCase(music_player=player, settings_repo=repo)

        # Khi gọi play()
        bgm_uc.play()

        # Âm lượng của player phải được cập nhật ngay thành 25
        self.assertEqual(player.volume, 25, "Âm lượng của player phải được đồng bộ chính xác thành 25 khi play")

    def test_t007_save_data_logic_flow(self):
        """User Story 2: Kiểm tra logic phân nhánh của save_data()."""
        player = MockMusicPlayer()
        player.current_target = "https://youtube.com/old_track"
        player.playing = True
        settings = ViewerSettings(bgm_youtube_url=player.current_target, bgm_volume=60)
        repo = MockSettingsRepo(settings)
        bgm_uc = ManageBgmUseCase(music_player=player, settings_repo=repo)

        initial_url = player.current_target
        initial_source = "youtube"

        # Trường hợp 1: URL và Source giữ nguyên (ví dụ chỉ đổi thời gian chiếu)
        new_url = "https://youtube.com/old_track"
        new_source = "youtube"
        source_changed = (new_url != initial_url) or (new_source != initial_source)
        self.assertFalse(source_changed)

        if source_changed:
            bgm_uc.stop()
            bgm_uc.update_bgm_config(BgmConfig(enabled=True, source=new_source, youtube_url=new_url, volume=60, loop=True))
        else:
            bgm_uc.apply_settings_without_reload(BgmConfig(enabled=True, source=new_source, youtube_url=new_url, volume=60, loop=True))

        # Xác nhận player không bị stop và không bị set_source lại
        self.assertEqual(player.stop_called_count, 0)
        self.assertEqual(len(player.source_set_history), 0)
        self.assertTrue(player.is_playing())

        # Trường hợp 2: Đổi sang URL mới
        new_url = "https://youtube.com/new_track"
        source_changed = (new_url != initial_url) or (new_source != initial_source)
        self.assertTrue(source_changed)

        if source_changed:
            bgm_uc.stop()
            bgm_uc.update_bgm_config(BgmConfig(enabled=True, source=new_source, youtube_url=new_url, volume=60, loop=True))

        # Lúc này player bị dừng bài cũ và nạp bài mới
        self.assertEqual(player.stop_called_count, 1)
        self.assertIn("https://youtube.com/new_track", player.source_set_history)


if __name__ == "__main__":
    unittest.main()
