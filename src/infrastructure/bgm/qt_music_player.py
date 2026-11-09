import os
from typing import Callable, Optional
from PyQt6.QtCore import QObject, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from src.domain.models import BgmPlaybackState
from src.domain.ports import MusicPlayerPort
from src.infrastructure.bgm.base_provider import BaseBgmProvider


class QtMusicPlayer(QObject):
    """
    Hiện thực MusicPlayerPort sử dụng PyQt6.QtMultimedia.
    Kết nối với BaseBgmProvider để hỗ trợ đa nguồn phát (YouTube, Local, etc.).
    Tích hợp quản lý trạng thái BgmPlaybackState và Safety Timeout 15s.
    """
    def __init__(self, provider: Optional[BaseBgmProvider] = None):
        super().__init__()
        self.provider = provider
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.current_target: str = ""
        self.current_stream_url: str = ""
        self._loop: bool = True
        self._volume: int = 70
        self.set_volume(self._volume)

        self.playback_state: BgmPlaybackState = BgmPlaybackState.STOPPED
        self._state_callback: Optional[Callable[[BgmPlaybackState, Optional[str]], None]] = None
        self._error_callback: Optional[Callable[[str], None]] = None
        self._status_callback: Optional[Callable[[str], None]] = None

        # Safety Timeout 15 giây khi nạp nguồn phát
        self.timeout_timer = QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.setInterval(15000)
        self.timeout_timer.timeout.connect(self._on_loading_timeout)

        # Kết nối sự kiện của QMediaPlayer
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)
        self.player.errorOccurred.connect(self._on_player_error)

    def _set_playback_state(self, state: BgmPlaybackState, msg: Optional[str] = None) -> None:
        self.playback_state = state
        if state != BgmPlaybackState.LOADING:
            self.timeout_timer.stop()
        if self._state_callback:
            self._state_callback(state, msg)

    def set_state_callback(self, callback: Callable[[BgmPlaybackState, Optional[str]], None]) -> None:
        self._state_callback = callback

    def cancel_loading(self) -> None:
        """Hủy tiến trình nạp nhạc nếu đang chờ."""
        self.timeout_timer.stop()
        if self.provider:
            self.provider.cancel()
        self._set_playback_state(BgmPlaybackState.STOPPED)

    def _on_loading_timeout(self) -> None:
        err = "Quá thời gian nạp nhạc (Timeout 15s). Vui lòng kiểm tra mạng hoặc link."
        if self.provider:
            self.provider.cancel()
        self.player.stop()
        self._set_playback_state(BgmPlaybackState.ERROR, err)
        if self._error_callback:
            self._error_callback(err)
        if self._status_callback:
            self._status_callback(f"Lỗi: {err}")

    def set_provider(self, provider: BaseBgmProvider) -> None:
        """Thay đổi bộ cung cấp nguồn phát (YouTube, Local, etc.)."""
        if self.provider:
            self.provider.cancel()
        self.provider = provider

    def set_source(self, source_target: str) -> None:
        """Thiết lập nguồn phát nhạc."""
        source_target = source_target.strip()
        if not source_target:
            self.stop()
            self.current_target = ""
            self.current_stream_url = ""
            self._set_playback_state(BgmPlaybackState.STOPPED)
            return

        if source_target == self.current_target and self.current_stream_url:
            return

        self.current_target = source_target
        self._set_playback_state(BgmPlaybackState.LOADING, "Đang kết nối luồng nhạc...")
        self.timeout_timer.start()

        if self.provider:
            if self._status_callback:
                self._status_callback("Đang kết nối luồng nhạc...")
            self.provider.prepare_source(
                target=source_target,
                on_ready=self._on_stream_ready,
                on_error=self._on_stream_error
            )
        else:
            if os.path.exists(source_target):
                self._on_stream_ready(source_target)
            else:
                self._on_stream_error("Không có provider phù hợp hoặc tệp không tồn tại.")

    def _on_stream_ready(self, stream_url: str) -> None:
        self.timeout_timer.stop()
        self.current_stream_url = stream_url
        if stream_url.startswith("http://") or stream_url.startswith("https://"):
            self.player.setSource(QUrl(stream_url))
        else:
            self.player.setSource(QUrl.fromLocalFile(stream_url))

        if self._status_callback:
            self._status_callback("Sẵn sàng phát nhạc.")
        self.player.play()
        self._set_playback_state(BgmPlaybackState.PLAYING)

    def _on_stream_error(self, err_msg: str) -> None:
        self.timeout_timer.stop()
        self._set_playback_state(BgmPlaybackState.ERROR, err_msg)
        if self._error_callback:
            self._error_callback(err_msg)
        if self._status_callback:
            self._status_callback(f"Lỗi: {err_msg}")

    def get_source(self) -> str:
        return self.current_target

    def play(self) -> None:
        if self.player.source().isEmpty() and self.current_target and self.provider:
            self.set_source(self.current_target)
            return
        if not self.current_target:
            return
        self.player.play()
        self._set_playback_state(BgmPlaybackState.PLAYING)

    def pause(self) -> None:
        self.timeout_timer.stop()
        self.player.pause()
        self._set_playback_state(BgmPlaybackState.STOPPED)

    def stop(self) -> None:
        self.timeout_timer.stop()
        self.player.stop()
        self._set_playback_state(BgmPlaybackState.STOPPED)

    def set_volume(self, volume: int) -> None:
        self._volume = max(0, min(100, volume))
        # QAudioOutput setVolume nhận giá trị float từ 0.0 đến 1.0
        self.audio_output.setVolume(self._volume / 100.0)

    def set_loop(self, loop: bool) -> None:
        self._loop = loop

    def is_playing(self) -> bool:
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def set_error_callback(self, callback: Callable[[str], None]) -> None:
        self._error_callback = callback

    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        self._status_callback = callback

    def _on_media_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self._loop:
                self.player.setPosition(0)
                self.player.play()
            else:
                self.player.stop()

    def _on_player_error(self, error: QMediaPlayer.Error, error_string: str) -> None:
        if error != QMediaPlayer.Error.NoError:
            if self._error_callback:
                self._error_callback(f"Lỗi phát nhạc: {error_string}")
