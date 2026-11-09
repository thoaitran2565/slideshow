# Engine Contract: Transition Engine & Strategies

**Feature**: `004-bgm-transform-transitions`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Hợp Đồng Chiến Lược Hiệu Ứng: `BaseTransitionStrategy`

```python
from abc import ABC, abstractmethod
from typing import Callable
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

class BaseTransitionStrategy(ABC):
    """Lớp chiến lược trừu tượng cho các hiệu ứng chuyển cảnh."""

    @abstractmethod
    def execute(
        self,
        view: QGraphicsView,
        current_item: QGraphicsPixmapItem,
        next_pixmap: QPixmap,
        direction: str,  # "forward" hoặc "backward"
        duration_ms: int,
        on_finished: Callable[[], None]
    ) -> None:
        """Thực thi chuyển cảnh giữa ảnh hiện tại và ảnh tiếp theo."""
        pass

    @abstractmethod
    def cancel(self) -> None:
        """Hủy an toàn hoạt ảnh đang chạy dở khi người dùng chuyển ảnh liên tục."""
        pass
```

---

## 2. Hợp Đồng Bộ Điều Phối: `TransitionEngine`

```python
class TransitionEngine:
    """Bộ điều phối quản lý và chuyển giao hiệu ứng chuyển cảnh."""

    def register_strategy(self, transition_type: str, strategy: BaseTransitionStrategy) -> None:
        """Đăng ký một chiến lược hiệu ứng mới vào động cơ."""
        pass

    def perform_transition(
        self,
        transition_type: str,
        view: QGraphicsView,
        current_item: QGraphicsPixmapItem,
        next_pixmap: QPixmap,
        direction: str,
        duration_ms: int,
        on_finished: Callable[[], None]
    ) -> None:
        """Chọn chiến lược đã đăng ký và thực thi hoạt ảnh."""
        pass
```

