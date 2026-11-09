# Research: Nâng Cao Tương Phản & Ghi Nhớ Trạng Thái

**Feature**: `002-control-panel-enhancement`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Kỹ Thuật Đổ Bóng & Tách Lớp Thị Giác Trong PyQt6

### Decision
Sử dụng `QGraphicsDropShadowEffect` gắn trực tiếp vào widget `ControlPanel` và nút `btn_show_panel`:
- `setBlurRadius(24)`
- `setOffset(0, 4)`
- `setColor(QColor(0, 0, 0, 210))`
- Kết hợp với QSS:
  ```css
  QWidget#ControlPanelRoot {
      background-color: rgba(18, 18, 18, 245);
      border: 2px solid rgba(255, 255, 255, 120);
      border-radius: 20px;
  }
  QPushButton {
      background-color: rgba(35, 35, 35, 230);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 80);
      font-weight: bold;
  }
  ```

### Rationale
- `QGraphicsDropShadowEffect` tạo vùng đổ bóng đen mềm mại xung quanh widget nổi, giúp mắt người dùng dễ dàng tách biệt thẻ nổi khỏi bất kỳ hình ảnh nào ở phía dưới (dù là ảnh tuyết trắng tinh hay ảnh nắng chói).
- Nền `#121212` với độ mờ đục 95% triệt tiêu hoàn toàn hiện tượng chói mắt hoặc chữ bị hòa lẫn vào pixel ảnh sáng màu bên dưới.

### Alternatives Considered
- *Bottom Gradient Scrim (dải chuyển màu tối đáy)*: Làm tối cả góc đáy của bức ảnh đang xem, làm mất tính trung thực của ảnh.
- *Thanh Dock cố định đáy*: Chiếm diện tích cố định, mất đi cảm giác hiện đại của phong cách Floating Card.

---

## 2. Chiến Lược Lưu Trữ Trạng Thái (Settings Persistence)

### Decision
Mở rộng thực thể `ViewerSettings` trong Domain và `JsonSettingsRepository` trong Infrastructure:
- Thêm trường `is_random: bool = False`
- Thêm trường `show_control_panel: bool = True`
- Cập nhật tự động vào `settings.json` ngay khi người dùng tương tác:
  - Bấm nút "🔀 Random": gọi `presenter.set_random(checked)` -> cập nhật playlist và lưu `settings.json`.
  - Bấm ẩn/hiện thanh công cụ (qua nút Ẩn, nút Hiện hoặc phím tắt `H`): gọi `presenter.set_panel_visibility(show_panel)` -> lưu `settings.json`.

### Rationale
- Thao tác lưu diễn ra bất đồng bộ/tức thời không gây trễ giao diện vì tệp `settings.json` rất nhỏ (<2KB).
- Người dùng không cần bấm nút "Lưu" thủ công, ứng dụng tự động ghi nhớ mọi tùy chọn ngay tại thời điểm thao tác.

