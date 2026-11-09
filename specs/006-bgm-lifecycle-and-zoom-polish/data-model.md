# Data Model: Tinh Chỉnh Vòng Đời Nhạc Nền & Mượt Mà Zoom Fade

**Feature**: `006-bgm-lifecycle-and-zoom-polish`
**Status**: Completed

## 1. Mô Hình Trạng Thái Phát Nhạc Nền (Domain / Application Layer)

### BgmPlaybackState
Enum biểu diễn các trạng thái hoạt động của dịch vụ nhạc nền:

```python
from enum import Enum

class BgmPlaybackState(Enum):
    STOPPED = "stopped"    # Nhạc đang tắt, sẵn sàng kích hoạt
    LOADING = "loading"    # Đang trích xuất luồng và kết nối (chờ tối đa 15s)
    PLAYING = "playing"    # Đang phát âm thanh ra loa
    ERROR = "error"        # Gặp sự cố kết nối, quá thời gian timeout hoặc link hỏng
```

### BgmConfig (Cập nhật)
Loại bỏ trường `enabled` không còn dùng (hoặc giữ làm fallback), tập trung vào dữ liệu nguồn:

```python
@dataclass
class BgmConfig:
    enabled: bool = True          # Luôn khả dụng nếu có link
    source: str = "youtube"       # Nguồn phát hợp lệ
    youtube_url: str = ""         # Link / ID video YouTube
    volume: int = 50              # Mức âm lượng (0 - 100)
    loop: bool = True             # Tự động lặp lại
```

---

## 2. Mô Hình Trạng Thái UI & Lớp Phủ (Presentation Layer)

### QuickVolumeModalState
Quản lý trạng thái hiển thị của popup âm lượng và lớp phủ chống click xuyên:

| Thuộc tính | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `popup_visible` | `bool` | Thanh trượt âm lượng có đang hiển thị hay không |
| `overlay_active` | `bool` | Lớp phủ trong suốt có đang chặn sự kiện hay không |
| `anchor_widget` | `QWidget` | Nút BGM làm điểm neo định vị popup |

### ZoomFadeNormalizationState
Thông số chuẩn hóa khung hình cho hiệu ứng Zoom Fade:

| Thuộc tính | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `viewport_rect` | `QRectF` | Kích thước khung nhìn hiện thời của `QGraphicsView` |
| `target_scale` | `float` | Hệ số thu phóng chuẩn hóa để ảnh mới vừa khít khung nhìn |
| `center_point` | `QPointF` | Điểm tâm khung nhìn dùng làm gốc biến đổi phóng to |

