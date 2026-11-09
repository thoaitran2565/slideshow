from typing import Callable
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

from src.presentation.views.transitions.base_transition import BaseTransitionStrategy


class InstantTransition(BaseTransitionStrategy):
    """Hiệu ứng chuyển cảnh tức thì (không có hoạt ảnh trễ)."""

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
        current_item.setPixmap(next_pixmap)
        incoming_item.setVisible(False)
        current_item.setVisible(True)
        if on_finished:
            on_finished()

    def cancel(self) -> None:
        pass

