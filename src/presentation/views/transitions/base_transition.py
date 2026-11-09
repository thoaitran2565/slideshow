from typing import Callable
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap


class BaseTransitionStrategy(QObject):
    """Lớp chiến lược cơ sở cho các hiệu ứng chuyển ảnh."""

    def execute(
        self,
        view: QGraphicsView,
        current_item: QGraphicsPixmapItem,
        incoming_item: QGraphicsPixmapItem,
        next_pixmap: QPixmap,
        direction: str,  # "forward" hoặc "backward"
        duration_ms: int,
        on_finished: Callable[[], None]
    ) -> None:
        """Thực thi chuyển cảnh giữa ảnh hiện tại và ảnh tiếp theo."""
        raise NotImplementedError

    def cancel(self) -> None:
        """Hủy an toàn hoạt ảnh đang chạy dở khi người dùng thao tác nhanh."""
        raise NotImplementedError
