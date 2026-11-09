from typing import Callable, Optional
from PyQt6.QtCore import QVariantAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

from src.presentation.views.transitions.base_transition import BaseTransitionStrategy


class CrossFadeTransition(BaseTransitionStrategy):
    """Hiệu ứng hòa tan / mờ dần (Cross-Fade mượt mà)."""

    def __init__(self):
        super().__init__()
        self._anim: Optional[QVariantAnimation] = None

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
        self.cancel()

        # Cài đặt ảnh mới vào incoming_item
        incoming_item.setPixmap(next_pixmap)
        incoming_item.setOpacity(0.0)
        incoming_item.setVisible(True)
        current_item.setOpacity(1.0)
        current_item.setVisible(True)

        self._anim = QVariantAnimation()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        def _on_value_changed(val: float):
            incoming_item.setOpacity(val)
            current_item.setOpacity(1.0 - val)

        def _on_finish():
            current_item.setPixmap(next_pixmap)
            current_item.setOpacity(1.0)
            incoming_item.setVisible(False)
            self._anim = None
            if on_finished:
                on_finished()

        self._anim.valueChanged.connect(_on_value_changed)
        self._anim.finished.connect(_on_finish)
        self._anim.start()

    def cancel(self) -> None:
        if self._anim and self._anim.state() == QVariantAnimation.State.Running:
            self._anim.stop()
            self._anim = None

