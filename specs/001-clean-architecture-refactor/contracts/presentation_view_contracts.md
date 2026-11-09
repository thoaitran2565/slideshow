# Presentation & View Contracts: UI Interaction Interfaces

**Feature**: `001-clean-architecture-refactor`  
**Date**: 2026-11-09  
**Status**: Draft  

---

## 1. Giao Diện Trừu Tượng Của Cửa Sổ Trình Chiếu (`PhotoViewerViewContract`)
Tầng Presenter/Controller sử dụng giao diện này để cập nhật trạng thái hiển thị tới `PhotoViewerWindow` mà không phụ thuộc vào chi tiết cài đặt của PyQt6.

```python
from typing import Protocol, Optional
from src.domain.models import ImageItem

class PhotoViewerViewContract(Protocol):
    def display_image(self, item: ImageItem) -> None:
        """Cập nhật ảnh hiển thị lên QGraphicsScene cùng hiệu ứng Fade animation."""
        ...

    def update_header_info(self, text: str) -> None:
        """Cập nhật nhãn hiển thị chỉ số ảnh và tên file ở góc trên bên trái."""
        ...

    def update_favorite_indicator(self, is_favorite: bool) -> None:
        """Cập nhật trạng thái biểu tượng trái tim đỏ hoặc trắng trên nút top-favorite."""
        ...

    def set_playing_state(self, is_playing: bool) -> None:
        """Đồng bộ trạng thái phát/tạm dừng trên nút ControlPanel và khởi động/dừng QTimer."""
        ...

    def show_empty_state(self) -> None:
        """Hiển thị thông báo khi thư mục không có ảnh hợp lệ."""
        ...

    def show_error_dialog(self, title: str, message: str) -> None:
        """Hiển thị thông báo lỗi người dùng qua QMessageBox."""
        ...
```

---

## 2. CLI Argument Contract
Quy định cách ứng dụng xử lý tham số dòng lệnh từ hệ điều hành:

```python
@dataclass(frozen=True)
class AppStartupArgs:
    target_file: Optional[str] = None
    target_dir: Optional[str] = None

def parse_startup_arguments(argv: list[str]) -> AppStartupArgs:
    """
    Phân tích sys.argv:
    - Nếu argv[1] là file ảnh hợp lệ: target_file = argv[1], target_dir = dirname(argv[1])
    - Nếu argv[1] là thư mục: target_dir = argv[1]
    - Ngược lại: target_file = None, target_dir = None
    """
```

