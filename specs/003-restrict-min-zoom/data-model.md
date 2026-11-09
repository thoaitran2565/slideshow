# Data Model: View Zoom State Representation

**Feature**: `003-restrict-min-zoom`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Trạng Thái Khung Nhìn (Presentation View State)

```python
class ZoomState:
    """Mô hình trạng thái mức zoom trong PhotoViewerWindow."""
    current_zoom: float = 1.0     # Mức zoom tương đối so với trạng thái Fit in View
    min_zoom: float = 1.0         # Ngưỡng chặn tối thiểu (Fit in View)
    max_zoom: float = 20.0        # Ngưỡng phóng đại tối đa an toàn
    zoom_step: float = 1.15       # Bước phóng đại mỗi nấc cuộn chuột
```

- **Validation & Clamping Rules**:
  - `min_zoom <= current_zoom <= max_zoom`
  - Khi `current_zoom == min_zoom` ($1.0$), trạng thái khung nhìn luôn được đồng bộ với `view.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)`.

