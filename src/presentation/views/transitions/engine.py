from typing import Dict, Callable, Optional
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

from src.domain.models import TransitionType
from src.presentation.views.transitions.base_transition import BaseTransitionStrategy


class TransitionEngine:
    """Bộ điều phối quản lý và chuyển giao các hiệu ứng chuyển cảnh."""

    def __init__(self):
        self._strategies: Dict[str, BaseTransitionStrategy] = {}
        self._active_strategy: Optional[BaseTransitionStrategy] = None

    def register_strategy(self, transition_type: str, strategy: BaseTransitionStrategy) -> None:
        """Đăng ký một chiến lược chuyển cảnh vào bộ điều phối."""
        self._strategies[transition_type.lower()] = strategy

    def cancel_active(self) -> None:
        """Hủy hoạt ảnh đang chạy dở để tránh xung đột chuyển slide nhanh."""
        if self._active_strategy:
            self._active_strategy.cancel()
            self._active_strategy = None

    def perform_transition(
        self,
        transition_type: str,
        view: QGraphicsView,
        current_item: QGraphicsPixmapItem,
        incoming_item: QGraphicsPixmapItem,
        next_pixmap: QPixmap,
        direction: str = "forward",
        duration_ms: int = 450,
        on_finished: Optional[Callable[[], None]] = None
    ) -> None:
        """Thực thi hiệu ứng chuyển cảnh được chỉ định."""
        self.cancel_active()

        key = transition_type.lower()
        strategy = self._strategies.get(key) or self._strategies.get(TransitionType.NONE)

        if not strategy:
            # Fallback đơn giản nếu chưa có strategy nào được đăng ký
            current_item.setPixmap(next_pixmap)
            if on_finished:
                on_finished()
            return

        self._active_strategy = strategy

        def _wrapped_on_finished():
            self._active_strategy = None
            if on_finished:
                on_finished()

        strategy.execute(
            view=view,
            current_item=current_item,
            incoming_item=incoming_item,
            next_pixmap=next_pixmap,
            direction=direction,
            duration_ms=duration_ms,
            on_finished=_wrapped_on_finished
        )

