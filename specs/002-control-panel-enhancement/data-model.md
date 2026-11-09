# Data Model: Control Panel State & Persistence

**Feature**: `002-control-panel-enhancement`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Mở Rộng Domain Entity: `ViewerSettings`

```python
@dataclass
class ViewerSettings:
    image_folder: str = ""
    interval_ms: int = 3000
    bg_color: str = "#000000"
    favorites: List[str] = field(default_factory=list)
    is_maximized: bool = False
    is_fullscreen: bool = False
    window_geometry: List[int] = field(default_factory=lambda: [100, 100, 1050, 720])
    
    # --- CÁC TRƯỜNG MỚI BỔ SUNG ---
    is_random: bool = False          # Lưu trạng thái bật/tắt chế độ phát ngẫu nhiên
    show_control_panel: bool = True  # Lưu trạng thái hiển thị của thanh điều khiển bên dưới
```

- **Validation Rules**:
  - `is_random` phải là giá trị boolean (`True` hoặc `False`). Mặc định nếu thiếu là `False`.
  - `show_control_panel` phải là giá trị boolean (`True` hoặc `False`). Mặc định nếu thiếu là `True`.

---

## 2. Ánh Xạ JSON (`settings.json`)

```json
{
    "image_folder": "D:/Photos",
    "interval_ms": 3000,
    "bg_color": "#000000",
    "favorites": [],
    "is_maximized": false,
    "is_fullscreen": false,
    "window_geometry": [100, 100, 1050, 720],
    "is_random": true,
    "show_control_panel": false
}
```

