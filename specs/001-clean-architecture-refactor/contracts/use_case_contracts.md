# Use Case Contracts: Application Layer Boundaries

**Feature**: `001-clean-architecture-refactor`  
**Date**: 2026-11-09  
**Status**: Draft  

---

## 1. `LoadImagesUseCase`
Nạp danh sách ảnh từ một thư mục hoặc tệp chỉ định, sắp xếp theo thứ tự số tự nhiên của Windows (Natural Sort).

- **Input Contract**:
  ```python
  @dataclass(frozen=True)
  class LoadImagesRequest:
      folder_path: str
      start_file: Optional[str] = None
  ```
- **Output Contract**:
  ```python
  @dataclass(frozen=True)
  class LoadImagesResponse:
      total_count: int
      current_item: Optional[ImageItem]
      playlist_info_text: str
  ```
- **Exceptions / Error Handling**:
  - Nếu thư mục không tồn tại: tạo thư mục và trả về `total_count = 0, current_item = None`.
  - Nếu `start_file` nằm ngoài danh mục quét: tự động chèn vào vị trí đầu tiên của danh sách để người dùng có thể xem ngay lập tức.

---

## 2. `NavigatePlaylistUseCase`
Chuyển tới ảnh kế tiếp hoặc quay lại ảnh trước đó, xử lý điều hướng tuần tự hoặc ngẫu nhiên có ghi nhớ lịch sử.

- **Input Contract**:
  ```python
  class NavigationDirection(Enum):
      NEXT = "next"
      PREV = "prev"

  @dataclass(frozen=True)
  class NavigateRequest:
      direction: NavigationDirection
  ```
- **Output Contract**:
  ```python
  @dataclass(frozen=True)
  class NavigateResponse:
      current_item: Optional[ImageItem]
      playlist_info_text: str
      has_images: bool
  ```

---

## 3. `DeleteImageUseCase`
Đưa tệp ảnh hiện tại vào Thùng rác Windows và chuyển tiếp sang ảnh kế tiếp.

- **Input Contract**:
  ```python
  @dataclass(frozen=True)
  class DeleteImageRequest:
      path: Optional[str] = None  # Nếu None thì dùng ảnh hiện tại
  ```
- **Output Contract**:
  ```python
  @dataclass(frozen=True)
  class DeleteImageResponse:
      success: bool
      deleted_path: str
      error_message: Optional[str]
      next_item: Optional[ImageItem]
      playlist_info_text: str
  ```

---

## 4. `ManageFavoritesUseCase`
Thêm hoặc bỏ tệp ảnh khỏi danh sách yêu thích và lưu cập nhật vào cấu hình.

- **Input Contract**:
  ```python
  @dataclass(frozen=True)
  class ToggleFavoriteRequest:
      file_path: str
  ```
- **Output Contract**:
  ```python
  @dataclass(frozen=True)
  class ToggleFavoriteResponse:
      file_path: str
      is_favorite: bool
      total_favorites: int
  ```

---

## 5. `ManageSettingsUseCase`
Nạp và lưu trữ cấu hình người dùng (`interval_ms`, `bg_color`, `image_folder`, `window_geometry`, `is_maximized`, `is_fullscreen`).

- **Input Contract**:
  ```python
  @dataclass(frozen=True)
  class UpdateSettingsRequest:
      settings: ViewerSettings
  ```
- **Output Contract**:
  ```python
  @dataclass(frozen=True)
  class SettingsResponse:
      settings: ViewerSettings
      is_valid: bool
  ```

