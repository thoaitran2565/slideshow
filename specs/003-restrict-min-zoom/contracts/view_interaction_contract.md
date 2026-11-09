# View Interaction Contract: Zoom Control

**Feature**: `003-restrict-min-zoom`  
**Date**: 2026-11-09  
**Status**: Draft  

---

## 1. Hợp Đồng Tương Tác Cuộn Chuột (`wheelEvent`)

```python
class ZoomControlContract:
    def handle_wheel_zoom(self, delta_y: int) -> None:
        """
        Xử lý sự kiện cuộn chuột:
        - Nếu delta_y > 0: Phóng to (Zoom In) với bước nhảy 1.15, trần tối đa 20.0x.
        - Nếu delta_y < 0:
            - Nếu current_zoom > 1.0: Thu nhỏ dần về mức Fit in View.
            - Nếu current_zoom <= 1.0: Bỏ qua (No-op), không thu nhỏ dưới kích thước Fit in View.
        """

    def reset_zoom_to_fit(self) -> None:
        """
        Đặt lại khung nhìn vừa khít màn hình:
        - Gọi fitInView(pixmap_item, KeepAspectRatio)
        - Đặt current_zoom = 1.0
        """
```

