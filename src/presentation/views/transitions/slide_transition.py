from typing import Callable, Optional
from PyQt6.QtCore import QVariantAnimation, QEasingCurve, QPointF
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

from src.presentation.views.transitions.base_transition import BaseTransitionStrategy


class SlideTransition(BaseTransitionStrategy):
    """
    Hiệu ứng trượt ngang (Slide Left / Slide Right).
    Tự động đảo ngược hướng khi người dùng lùi ảnh (Prev).
    """

    def __init__(self, slide_to_left: bool = True):
        super().__init__()
        self.slide_to_left = slide_to_left
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

        # Tính toán hướng trượt thực tế (đảo chiều khi lùi ảnh)
        effective_slide_left = self.slide_to_left
        if direction == "backward":
            effective_slide_left = not effective_slide_left

        rect = view.viewport().rect()
        width = float(rect.width() if rect.width() > 0 else 800)

        # Cài đặt ảnh cho incoming_item
        incoming_item.setPixmap(next_pixmap)
        incoming_item.setOpacity(1.0)
        incoming_item.setVisible(True)
        current_item.setOpacity(1.0)
        current_item.setVisible(True)

        # Điểm bắt đầu
        start_x_incoming = width if effective_slide_left else -width
        end_x_current = -width if effective_slide_left else width

        incoming_item.setPos(start_x_incoming, 0)
        current_item.setPos(0, 0)

        self._anim = QVariantAnimation()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        def _on_value_changed(val: float):
            current_item.setPos(end_x_current * val, 0)
            incoming_item.setPos(start_x_incoming * (1.0 - val), 0)

        def _on_finish():
            current_item.setPixmap(next_pixmap)
            current_item.setPos(0, 0)
            incoming_item.setPos(0, 0)
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

