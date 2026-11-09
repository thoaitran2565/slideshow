from typing import Callable, Optional
from PyQt6.QtCore import QVariantAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QTransform

from src.presentation.views.transitions.base_transition import BaseTransitionStrategy


class ZoomFadeTransition(BaseTransitionStrategy):
    """Hiệu ứng phóng to nhẹ nhàng kết hợp hòa tan mờ dần (Zoom Fade) đồng tâm mượt mà."""

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

        incoming_item.setPixmap(next_pixmap)
        incoming_item.setOpacity(0.0)
        incoming_item.setVisible(True)
        current_item.setOpacity(1.0)
        current_item.setVisible(True)

        curr_rect = current_item.boundingRect()
        curr_w = max(1.0, curr_rect.width())
        curr_h = max(1.0, curr_rect.height())
        cx = curr_w / 2.0
        cy = curr_h / 2.0

        next_w = max(1.0, float(next_pixmap.width()))
        next_h = max(1.0, float(next_pixmap.height()))

        # Tính toán tỉ lệ chuẩn hóa base scale để ảnh mới vừa vặn tương ứng với khung nhìn hiện tại
        scale_fit = min(curr_w / next_w, curr_h / next_h)
        # Tọa độ bù lệch để tâm ảnh mới trùng khít tuyệt đối với tâm ảnh cũ
        offset_x = cx - (next_w * scale_fit) / 2.0
        offset_y = cy - (next_h * scale_fit) / 2.0

        self._anim = QVariantAnimation()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        def _on_value_changed(val: float):
            # 1. Ảnh cũ phóng to nhẹ từ 1.0 lên 1.05 quanh tâm cx, cy
            scale_old = 1.0 + (0.05 * val)
            t_old = QTransform()
            t_old.translate(cx, cy)
            t_old.scale(scale_old, scale_old)
            t_old.translate(-cx, -cy)
            current_item.setTransform(t_old)
            current_item.setOpacity(max(0.0, 1.0 - val))

            # 2. Ảnh mới thu phóng mượt mà từ 0.95*scale_fit về 1.0*scale_fit đồng tâm cx, cy
            scale_new_factor = 0.95 + (0.05 * val)
            cur_scale = scale_fit * scale_new_factor
            t_new = QTransform()
            t_new.translate(cx, cy)
            t_new.scale(scale_new_factor, scale_new_factor)
            t_new.translate(-cx, -cy)
            t_new.translate(offset_x, offset_y)
            t_new.scale(scale_fit, scale_fit)
            incoming_item.setTransform(t_new)
            incoming_item.setOpacity(min(1.0, val))

        def _on_finish():
            current_item.setTransform(QTransform())
            current_item.setPixmap(next_pixmap)
            current_item.setOpacity(1.0)
            incoming_item.setVisible(False)
            incoming_item.setTransform(QTransform())
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

