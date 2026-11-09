# Service Contract: Music Player & BGM Providers

**Feature**: `004-bgm-transform-transitions`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Domain Port: `MusicPlayerPort` (`src/domain/ports.py`)

Cổng giao tiếp trừu tượng thuần túy Python (không phụ thuộc framework):

```python
from abc import ABC, abstractmethod
from typing import Callable, Optional

class MusicPlayerPort(ABC):
    """Cổng giao tiếp điều khiển nhạc nền trừu tượng."""

    @abstractmethod
    def set_source(self, source_target: str) -> None:
        """Thiết lập nguồn phát nhạc (URL, đường dẫn tệp, hoặc định danh tài nguyên)."""
        pass

    @abstractmethod
    def play(self) -> None:
        """Bắt đầu hoặc tiếp tục phát nhạc."""
        pass

    @abstractmethod
    def pause(self) -> None:
        """Tạm dừng phát nhạc."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Dừng hoàn toàn phát nhạc."""
        pass

    @abstractmethod
    def set_volume(self, volume: int) -> None:
        """Đặt âm lượng từ 0 đến 100."""
        pass

    @abstractmethod
    def set_loop(self, loop: bool) -> None:
        """Bật/tắt chế độ lặp lại bài hát."""
        pass

    @abstractmethod
    def is_playing(self) -> bool:
        """Kiểm tra trạng thái đang phát nhạc."""
        pass

    @abstractmethod
    def set_error_callback(self, callback: Callable[[str], None]) -> None:
        """Đăng ký hàm xử lý khi có lỗi xảy ra."""
        pass

    @abstractmethod
    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        """Đăng ký hàm thông báo trạng thái (Đang tải, Sẵn sàng, v.v.)."""
        pass
```

---

## 2. Infrastructure Provider Contract: `BgmProvider`

Mỗi nguồn phát (YouTube, Local Files, Spotify) tuân thủ lớp cơ sở Provider:

```python
class BaseBgmProvider(ABC):
    @abstractmethod
    def prepare_source(self, target: str, on_ready: Callable[[str], None], on_error: Callable[[str], None]) -> None:
        """Chuẩn bị nguồn phát bất đồng bộ (trích xuất stream URL cho YouTube, kiểm tra file cho Local)."""
        pass
```

