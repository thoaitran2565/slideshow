# Research: Kiểm Soát Hệ Số Phóng Đại & Khóa Ngưỡng Thu Nhỏ (Zoom Clamp)

**Feature**: `003-restrict-min-zoom`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Nghiên Cứu Quản Lý Tỷ Lệ Scale Trong `QGraphicsView`

### Decision
Sử dụng biến theo dõi hệ số phóng đại tương đối `current_zoom: float` (với mốc cơ sở `1.0` tại trạng thái `fitInView`):
- Khi nạp ảnh (`show_image`) hoặc thay đổi kích thước cửa sổ (`resizeEvent`), gọi `fit_image_in_view()` và gán `current_zoom = 1.0`.
- Trong `wheelEvent`:
  - **Cuộn lên (`angleDelta().y() > 0`)**:
    - Nhân hệ số `1.15`, kẹp cận trên tại `20.0x`.
    - Gọi `self.view.scale(actual_factor, actual_factor)`.
    - Bật chế độ kéo rê `QGraphicsView.DragMode.ScrollHandDrag`.
  - **Cuộn xuống (`angleDelta().y() < 0`)**:
    - Nếu `current_zoom <= 1.001`: Không thực hiện scale (No-op), ngăn tuyệt đối việc thu nhỏ ảnh nhỏ hơn kích thước khung nhìn.
    - Nếu `current_zoom > 1.001`: Tính toán tỷ lệ mới `new_zoom = current_zoom / 1.15`.
      - Nếu `new_zoom <= 1.0`: Gọi trực tiếp `self.fit_image_in_view()` để đưa ảnh về vị trí trung tâm chuẩn xác và đặt `current_zoom = 1.0`.
      - Nếu `new_zoom > 1.0`: Thực hiện `self.view.scale(new_zoom / current_zoom, ...)` và cập nhật `current_zoom = new_zoom`.

### Rationale
- Việc kiểm soát hệ số zoom tương đối độc lập với ma trận pixel tuyệt đối giúp thuật toán hoạt động chính xác cho mọi độ phân giải ảnh (từ ảnh biểu tượng 64x64 đến ảnh 8K 7680x4320).
- Khi chạm ngưỡng $1.0x$, việc gọi `fit_image_in_view()` thay vì scale thủ công bảo đảm ảnh được căn giữa hoàn hảo và loại bỏ mọi sai số tích lũy dấu phẩy động (floating-point drift).

### Alternatives Considered
- *Kiểm tra ma trận biến đổi `transform().m11()` so với kích thước gốc*: Dễ gặp sai số làm tròn số học và phức tạp khi cửa sổ resize hoặc khi đổi giữa ảnh dọc và ảnh ngang.
- *Chỉ bỏ qua hoàn toàn sự kiện cuộn xuống (không cho thu nhỏ khi đã zoom in)*: Trải nghiệm người dùng sẽ bị hỏng vì một khi đã zoom to thì không thể quay trở lại nhìn toàn cảnh ảnh được nữa.

---

## 2. Kiến Trúc Phân Tầng

### Decision
Toàn bộ logic xử lý tỷ lệ zoom và ma trận biến đổi đồ họa được giới hạn hoàn toàn trong lớp `PhotoViewerWindow` thuộc tầng **Presentation (`src/presentation/views/viewer_window.py`)**.

### Rationale
- Tỷ lệ zoom khung nhìn là chi tiết tương tác giao diện (View Interaction detail), không phải nghiệp vụ lưu trữ dữ liệu (Domain Business Rule).
- Không làm thay đổi Domain Entities, Use Cases hay Repositories, giữ nguyên vẹn 100% kiến trúc Clean Architecture theo Hiến pháp dự án.

