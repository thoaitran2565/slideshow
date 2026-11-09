# Data Model: Clean Architecture Entities & State

**Feature**: `001-clean-architecture-refactor`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Domain Entities & Value Objects

### 1.1 `ImageItem` (Entity)
Đại diện cho một bức ảnh trong danh sách trình chiếu.
```python
@dataclass(frozen=True)
class ImageItem:
    path: str              # Đường dẫn tuyệt đối chuẩn hóa (os.path.abspath)
    filename: str          # Tên tệp (os.path.basename)
    is_favorite: bool      # Trạng thái có trong danh sách yêu thích hay không
```
- **Validation**:
  - `path` không được rỗng, phải có đuôi mở rộng hợp lệ nằm trong danh mục hỗ trợ (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.webp`).
- **Identity**: Xác định duy nhất thông qua đường dẫn chuẩn hóa `os.path.normcase(path)`.

---

### 1.2 `Playlist` (Aggregate Root / State Entity)
Đại diện cho tập hợp ảnh và trạng thái điều hướng của phiên xem hiện tại.
```python
@dataclass
class Playlist:
    items: list[ImageItem] = field(default_factory=list)
    current_index: int = 0
    is_random: bool = False
    history: list[int] = field(default_factory=list)
```
- **State Transitions**:
  - `next()`:
    - Nếu `is_random == False`: `current_index = (current_index + 1) % len(items)`.
    - Nếu `is_random == True`: lưu `current_index` vào `history`, chọn ngẫu nhiên index mới khác index hiện tại (nếu `len(items) > 1`).
  - `prev()`:
    - Nếu `is_random == True` và `history` không rỗng: `current_index = history.pop()`.
    - Ngược lại: `current_index = (current_index - 1) % len(items)`.
  - `remove_current()`:
    - Xóa phần tử tại `current_index`.
    - Nếu danh sách còn ảnh: `current_index = current_index % len(items)`.
    - Nếu danh sách rỗng: `current_index = -1`.

---

### 1.3 `ViewerSettings` (Entity / Value Object)
Lưu trữ toàn bộ thông tin cấu hình người dùng.
```python
@dataclass
class ViewerSettings:
    image_folder: str = ""
    interval_ms: int = 3000
    bg_color: str = "#000000"
    favorites: list[str] = field(default_factory=list)
    is_maximized: bool = False
    is_fullscreen: bool = False
    window_geometry: list[int] = field(default_factory=lambda: [100, 100, 1050, 720])
```
- **Validation Rules**:
  - `interval_ms` phải là số nguyên $\ge 1000$ (tối thiểu 1 giây).
  - `bg_color` phải là mã màu Hex hợp lệ (ví dụ `#000000`, `#ffffff`).
  - `window_geometry` phải là mảng 4 số nguyên `[x, y, width, height]` với `width >= 400`, `height >= 300`.

---

## 2. Ports (Giao Diện Trừu Tượng Tầng Domain)

```python
from typing import Protocol, Optional

class ImageRepositoryPort(Protocol):
    def scan_images(self, folder: str, supported_extensions: tuple[str, ...]) -> list[str]: ...
    def delete_image(self, path: str) -> tuple[bool, str]: ...

class SettingsRepositoryPort(Protocol):
    def load_settings(self) -> ViewerSettings: ...
    def save_settings(self, settings: ViewerSettings) -> None: ...

class SystemIntegrationPort(Protocol):
    def register_file_associations(self, exe_path: str) -> None: ...
    def reveal_in_explorer(self, path: str) -> None: ...
    def copy_to_clipboard(self, text: str) -> None: ...
```

---

## 3. Quan Hệ Giữa Các Tầng (Dependency Flow)

```text
+-------------------------------------------------------------+
| Presentation (Views: PyQt6 Windows, Dialogs, Presenter)      |
+------------------------------+------------------------------+
                               | calls
                               v
+-------------------------------------------------------------+
| Application (Use Cases: Load, Navigate, Delete, Settings)   |
+------------------------------+------------------------------+
                               | depends on
                               v
+-------------------------------------------------------------+
| Domain (Entities: ImageItem, Playlist, Settings; Ports)     |
+------------------------------+------------------------------+
                               ^ implements ports
                               |
+-------------------------------------------------------------+
| Infrastructure (JsonSettingsRepo, LocalImageRepo, WinAdapter)|
+-------------------------------------------------------------+
```

