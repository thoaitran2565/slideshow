# Contracts: Tinh Chỉnh Vòng Đời Nhạc Nền & Mượt Mà Zoom Fade

**Feature**: `006-bgm-lifecycle-and-zoom-polish`
**Status**: Completed

## 1. Music Player Port & Loading Timeout Contract

Cổng trừu tượng `MusicPlayerPort` bổ sung quản lý trạng thái loading và timeout:

```python
class MusicPlayerPort(Protocol):
    def get_playback_state(self) -> BgmPlaybackState: ...
    def set_state_callback(self, cb: Callable[[BgmPlaybackState, Optional[str]], None]) -> None: ...
    def cancel_loading(self) -> None: ...
```

- Khi nạp nhạc: Phát ra `(BgmPlaybackState.LOADING, None)`.
- Khi nạp quá 15s hoặc lỗi: Hủy luồng, phát ra `(BgmPlaybackState.ERROR, "Quá thời gian nạp nhạc (Timeout 15s)")`.
- Khi bắt đầu phát: Phát ra `(BgmPlaybackState.PLAYING, None)`.
- Khi tắt nhạc: Phát ra `(BgmPlaybackState.STOPPED, None)`.

---

## 2. Backdrop Overlay Contract

Giao diện lớp phủ chống click xuyên:

```python
class BackdropOverlay(QWidget):
    """Lớp phủ trong suốt bao trùm toàn bộ cửa sổ chính."""
    dismissed = pyqtSignal()

    def __init__(self, parent: QWidget): ...
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # Tiêu thụ sự kiện, đóng popup và phát tín hiệu dismissed
        event.accept()
        self.dismissed.emit()
```

---

## 3. Zoom Fade Transition Strategy Contract

Hiệu ứng Zoom Fade chuẩn hóa khung nhìn trước khi hoạt ảnh:

```python
class ZoomFadeTransition(BaseTransitionStrategy):
    def execute(
        self,
        view: QGraphicsView,
        current_item: QGraphicsPixmapItem,
        incoming_item: QGraphicsPixmapItem,
        next_pixmap: QPixmap,
        direction: str,
        duration_ms: int,
        on_finished: Callable[[], None]
    ) -> None:
        """
        1. Tiền xử lý tính toán tỉ lệ fit vừa khít viewport của view.
        2. Đặt incoming_item đúng vị trí trung tâm scene.
        3. Chạy hoạt ảnh mờ dần kết hợp scale nhẹ quanh tâm đồng bộ ở 60 FPS.
        4. Kết thúc và dọn dẹp an toàn.
        """
        ...
```

