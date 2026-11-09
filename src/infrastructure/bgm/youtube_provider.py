import re
from typing import Callable, Optional
from PyQt6.QtCore import QThread, pyqtSignal
import yt_dlp

from src.infrastructure.bgm.base_provider import BaseBgmProvider


class YouTubeStreamWorker(QThread):
    """Worker chạy ngầm trích xuất URL luồng audio trực tiếp từ YouTube mà không block UI."""
    ready = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, target: str):
        super().__init__()
        self.target = target.strip()
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        if not self.target:
            self.error.emit("Vui lòng cung cấp URL hoặc Video ID YouTube.")
            return

        # Chuẩn hóa nếu người dùng chỉ nhập Video ID (11 ký tự)
        url = self.target
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
            url = f"https://www.youtube.com/watch?v={url}"

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'socket_timeout': 10,
            'ignoreerrors': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if self._is_cancelled:
                    return
                info = ydl.extract_info(url, download=False)
                if self._is_cancelled:
                    return

                if not info:
                    self.error.emit("Không tìm thấy thông tin video.")
                    return

                # Nếu là playlist, lấy phần tử đầu tiên
                if 'entries' in info and info['entries']:
                    for entry in info['entries']:
                        if entry:
                            info = entry
                            break

                stream_url = info.get('url')
                if not stream_url and 'formats' in info:
                    # Tìm format audio tốt nhất
                    for fmt in reversed(info['formats']):
                        if fmt.get('url') and (fmt.get('acodec') != 'none' or fmt.get('vcodec') == 'none'):
                            stream_url = fmt['url']
                            break

                if stream_url:
                    self.ready.emit(stream_url)
                else:
                    self.error.emit("Không thể trích xuất luồng âm thanh từ video này.")
        except Exception as e:
            if not self._is_cancelled:
                err_str = str(e)
                # Đơn giản hóa thông báo lỗi cho người dùng dễ hiểu
                if "Incomplete YouTube ID" in err_str or "Video unavailable" in err_str:
                    clean_msg = "Video không tồn tại hoặc đã bị gỡ bỏ."
                elif "timed out" in err_str.lower() or "network" in err_str.lower() or "connection" in err_str.lower():
                    clean_msg = "Không thể kết nối đến YouTube (hết thời gian chờ hoặc mất mạng)."
                else:
                    clean_msg = f"Lỗi nạp YouTube: {err_str[:80]}"
                self.error.emit(clean_msg)


class YouTubeBgmProvider(BaseBgmProvider):
    """Hiện thực BaseBgmProvider cho nguồn nhạc YouTube trực tuyến."""

    def __init__(self):
        self._worker: Optional[YouTubeStreamWorker] = None

    def prepare_source(
        self,
        target: str,
        on_ready: Callable[[str], None],
        on_error: Callable[[str], None]
    ) -> None:
        self.cancel()

        self._worker = YouTubeStreamWorker(target)

        def _on_ready_wrapper(stream_url: str):
            on_ready(stream_url)
            self._worker = None

        def _on_error_wrapper(err_msg: str):
            on_error(err_msg)
            self._worker = None

        self._worker.ready.connect(_on_ready_wrapper)
        self._worker.error.connect(_on_error_wrapper)
        self._worker.start()

    def cancel(self) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.cancel()
            self._worker.quit()
            self._worker.wait(1000)
            self._worker = None

