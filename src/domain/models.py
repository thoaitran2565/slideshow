from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import os
import random

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')


class BgmPlaybackState(Enum):
    """Trạng thái vòng đời phát nhạc nền."""
    STOPPED = "stopped"
    LOADING = "loading"
    PLAYING = "playing"
    ERROR = "error"


@dataclass(frozen=True)
class ImageItem:
    """Đại diện cho một tệp ảnh trong hệ thống."""
    path: str
    filename: str
    is_favorite: bool = False

    def __post_init__(self):
        if not self.path or not self.path.strip():
            raise ValueError("Đường dẫn tệp ảnh không được để trống")
        ext = os.path.splitext(self.path)[1].lower()
        if ext and ext not in SUPPORTED_EXTENSIONS:
            # Cho phép tạo đối tượng nếu tệp nằm trong danh sách mở rộng hợp lệ
            pass


@dataclass
class Playlist:
    """Quản lý tập hợp danh sách ảnh và trạng thái điều hướng của phiên xem."""
    items: List[ImageItem] = field(default_factory=list)
    current_index: int = 0
    is_random: bool = False
    history: List[int] = field(default_factory=list)

    @property
    def total_count(self) -> int:
        return len(self.items)

    @property
    def current_item(self) -> Optional[ImageItem]:
        if not self.items or self.current_index < 0 or self.current_index >= len(self.items):
            return None
        return self.items[self.current_index]

    def next(self) -> Optional[ImageItem]:
        """Chuyển sang ảnh kế tiếp."""
        if not self.items:
            return None
        if self.is_random:
            self.history.append(self.current_index)
            if len(self.items) > 1:
                # Chọn ngẫu nhiên index mới khác index hiện tại
                available_indices = [i for i in range(len(self.items)) if i != self.current_index]
                self.current_index = random.choice(available_indices)
            else:
                self.current_index = 0
        else:
            self.current_index = (self.current_index + 1) % len(self.items)
        return self.current_item

    def prev(self) -> Optional[ImageItem]:
        """Quay lại ảnh trước đó."""
        if not self.items:
            return None
        if self.is_random and self.history:
            self.current_index = self.history.pop()
        else:
            self.current_index = (self.current_index - 1) % len(self.items)
        return self.current_item

    def remove_current(self) -> Optional[ImageItem]:
        """Xóa ảnh hiện tại khỏi playlist và cập nhật lại con trỏ."""
        if not self.items or self.current_index < 0 or self.current_index >= len(self.items):
            return None
        del self.items[self.current_index]
        if self.items:
            self.current_index %= len(self.items)
            return self.current_item
        self.current_index = 0
        return None

    def get_info_text(self) -> str:
        """Sinh chuỗi thông tin hiển thị trạng thái danh sách."""
        if not self.items:
            return "Không có ảnh"
        curr = self.current_item
        filename = curr.filename if curr else ""
        if self.is_random:
            return f"🔀 Random - {filename}"
        return f"{self.current_index + 1} / {len(self.items)} - {filename}"


@dataclass
class BgmConfig:
    """Cấu hình phát nhạc nền đa nguồn."""
    enabled: bool = False
    source: str = "youtube"            # "youtube", "local", "spotify"
    youtube_url: str = ""             # URL hoặc Video ID YouTube
    volume: int = 70                  # 0 - 100
    loop: bool = True                 # Tự động lặp lại khi kết thúc bài


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


class TransitionType:
    """Danh mục hằng số các kiểu hiệu ứng chuyển cảnh."""
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_FADE = "zoom_fade"
    NONE = "none"

    ALL_TYPES = [FADE, SLIDE_LEFT, SLIDE_RIGHT, ZOOM_FADE, NONE]


class TransitionDirection:
    """Hướng chuyển cảnh."""
    FORWARD = "forward"   # Tiến (Next / Auto Slideshow)
    BACKWARD = "backward" # Lùi (Prev)


@dataclass
class ViewerSettings:
    """Lưu trữ cấu hình ứng dụng."""
    image_folder: str = ""
    interval_ms: int = 3000
    bg_color: str = "#000000"
    favorites: List[str] = field(default_factory=list)
    is_maximized: bool = False
    is_fullscreen: bool = False
    window_geometry: List[int] = field(default_factory=lambda: [100, 100, 1050, 720])
    is_random: bool = False
    show_control_panel: bool = True
    # Bổ sung cấu hình tính năng 004
    bgm_enabled: bool = False
    bgm_source: str = "youtube"
    bgm_youtube_url: str = ""
    bgm_volume: int = 70
    bgm_loop: bool = True
    transition_type: str = "fade"

    def __post_init__(self):
        # Ràng buộc dữ liệu tối thiểu
        if self.interval_ms < 1000:
            self.interval_ms = 1000
        if not self.window_geometry or len(self.window_geometry) != 4:
            self.window_geometry = [100, 100, 1050, 720]
        else:
            # Đảm bảo width >= 400, height >= 300
            self.window_geometry[2] = max(400, self.window_geometry[2])
            self.window_geometry[3] = max(300, self.window_geometry[3])

