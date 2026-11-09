# Data Model: Multimedia, Transform & Transitions

**Feature**: `004-bgm-transform-transitions`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Domain Entities & Value Objects (`src/domain/models.py`)

### A. Cấu Hình Dịch Vụ Nhạc Nền (`BgmConfig`)
```python
@dataclass
class BgmConfig:
    """Cấu hình phát nhạc nền đa nguồn."""
    enabled: bool = False
    source: str = "youtube"            # "youtube", "local", "spotify"
    youtube_url: str = ""             # URL hoặc Video ID YouTube
    volume: int = 70                  # 0 - 100
    loop: bool = True                 # Tự động lặp lại khi kết thúc bài
```

### B. Trạng Thái Biến Đổi Hình Học Ảnh (`ImageTransformState`)
```python
@dataclass
class ImageTransformState:
    """Trạng thái xoay và lật hiển thị của một bức ảnh trong phiên."""
    rotation_degrees: int = 0         # 0, 90, 180, 270
    flip_h: bool = False              # Lật ngang (Horizontal Flip)
    flip_v: bool = False              # Lật dọc (Vertical Flip)

    def rotate_cw(self) -> None:
        """Xoay thuận chiều kim đồng hồ 90 độ."""
        self.rotation_degrees = (self.rotation_degrees + 90) % 360

    def rotate_ccw(self) -> None:
        """Xoay ngược chiều kim đồng hồ 90 độ."""
        self.rotation_degrees = (self.rotation_degrees - 90) % 360

    def toggle_flip_h(self) -> None:
        """Đảo trạng thái lật ngang."""
        self.flip_h = not self.flip_h

    def toggle_flip_v(self) -> None:
        """Đảo trạng thái lật dọc."""
        self.flip_v = not self.flip_v

    def reset(self) -> None:
        """Đặt lại biến đổi về mặc định ban đầu."""
        self.rotation_degrees = 0
        self.flip_h = False
        self.flip_v = False

    @property
    def is_default(self) -> bool:
        return self.rotation_degrees == 0 and not self.flip_h and not self.flip_v
```

### C. Kiểu Hiệu Ứng Chuyển Cảnh (`TransitionType`)
```python
class TransitionType:
    """Danh mục hằng số các kiểu hiệu ứng chuyển cảnh."""
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_FADE = "zoom_fade"
    NONE = "none"

    ALL_TYPES = [FADE, SLIDE_LEFT, SLIDE_RIGHT, ZOOM_FADE, NONE]
```

### D. Hướng Chuyển Động (`TransitionDirection`)
```python
class TransitionDirection:
    """Hướng chuyển cảnh."""
    FORWARD = "forward"   # Tiến (Next / Auto Slideshow)
    BACKWARD = "backward" # Lùi (Prev)
```

---

## 2. Mở Rộng Cấu Hình Người Dùng (`ViewerSettings`)

Cập nhật các trường cấu hình trong thực thể `ViewerSettings` (`src/domain/models.py`) và tệp `settings.json`:

```python
@dataclass
class ViewerSettings:
    image_folder: str = ""
    interval_ms: int = 4000
    bg_color: str = "#000000"
    is_random: bool = False
    is_maximized: bool = False
    is_fullscreen: bool = False
    window_geometry: Optional[list[int]] = None
    is_control_panel_visible: bool = True
    
    # --- Mở rộng tính năng 004 ---
    bgm_enabled: bool = False
    bgm_source: str = "youtube"
    bgm_youtube_url: str = ""
    bgm_volume: int = 70
    bgm_loop: bool = True
    transition_type: str = "fade"      # "fade", "slide_left", "slide_right", "zoom_fade", "none"
```

