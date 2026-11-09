from abc import ABC, abstractmethod
from typing import Callable, Optional


class BaseBgmProvider(ABC):
    """Lớp cơ sở trừu tượng cho các nhà cung cấp nguồn phát nhạc nền (YouTube, Local, Spotify)."""

    @abstractmethod
    def prepare_source(
        self,
        target: str,
        on_ready: Callable[[str], None],
        on_error: Callable[[str], None]
    ) -> None:
        """
        Chuẩn bị nguồn phát bất đồng bộ.
        - target: URL hoặc đường dẫn tệp.
        - on_ready(stream_url): Callback khi đã sẵn sàng URL luồng phát.
        - on_error(err_msg): Callback khi gặp lỗi xử lý.
        """
        pass

    @abstractmethod
    def cancel(self) -> None:
        """Hủy tác vụ đang chạy ngầm nếu người dùng đổi bài hoặc tắt app."""
        pass

