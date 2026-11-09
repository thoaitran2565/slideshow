# Quickstart & Verification Guide: Clean Architecture Refactor

**Feature**: `001-clean-architecture-refactor`  
**Date**: 2026-11-09  
**Status**: Ready for Implementation  

---

## 1. Môi Trường & Điều Kiện Tiên Quyết
- Hệ điều hành: Windows 10/11
- Python 3.10+ đã được cài đặt và thêm vào PATH
- Thư viện phụ thuộc:
  ```powershell
  python -m pip install PyQt6 send2trash pyinstaller
  ```

---

## 2. Kịch Bản Kiểm Thử & Xác Thực (End-to-End Validation Scenarios)

### Kịch Bản 1: Kiểm thử Độc Lập Tầng Nghiệp Vụ (Pure Domain/Application Test)
Mục tiêu: Đảm bảo tầng Domain và Use Cases hoạt động độc lập không cần giao diện Qt.
- **Lệnh thực thi**:
  ```powershell
  python -c "from src.domain.models import ImageItem, Playlist; p = Playlist(); print('Domain OK')"
  ```
- **Kết quả kỳ vọng**: In ra `Domain OK` mà không có bất kỳ lỗi import hay cảnh báo nào liên quan đến `PyQt6`.

---

### Kịch Bản 2: Khởi Chạy Ứng Dụng Xem Ảnh Từ Mã Nguồn
Mục tiêu: Đảm bảo toàn bộ trải nghiệm người dùng, phím tắt, splash screen và animation hoạt động hoàn hảo.
- **Lệnh thực thi**:
  ```powershell
  python main.py
  ```
- **Kiểm tra tương tác**:
  1. Splash screen hiển thị thanh tiến trình loading mượt mà.
  2. Cửa sổ chính mở ra với các nút nổi Dark Theme, hiển thị ảnh mẫu đầu tiên.
  3. Bấm phím cách (Space) để Tạm dừng/Tiếp tục trình chiếu; dùng mũi tên Trái/Phải để chuyển ảnh.
  4. Cuộn chuột để phóng to/thu nhỏ, giữ chuột trái kéo ảnh trong khung nhìn.
  5. Bấm `F11` để bật/tắt chế độ toàn màn hình; bấm `Esc` để thoát.
  6. Bấm nút ❤️ ở góc trên bên phải để thêm/bỏ ảnh khỏi bộ sưu tập yêu thích.
  7. Nhấp chuột vào nút ⋮ (Option) > Xóa ảnh > xác nhận đưa vào Recycle Bin thành công.

---

### Kịch Bản 3: Kiểm thử Khởi Động Qua Dòng Lệnh ("Open with" Simulation)
Mục tiêu: Xác nhận việc mở tệp ảnh trực tiếp từ File Explorer hoạt động chính xác.
- **Lệnh thực thi**:
  ```powershell
  python main.py "images\sample1.jpg"
  ```
- **Kết quả kỳ vọng**: Ứng dụng khởi động ngay lập tức và nạp đúng ảnh `sample1.jpg`, đồng thời quét tất cả các ảnh khác trong thư mục `images/` vào danh sách duyệt.

---

### Kịch Bản 4: Kiểm Thử Đóng Gói Tệp Thực Thi (.EXE)
Mục tiêu: Xác nhận việc đóng gói PyInstaller thành tệp duy nhất không bị thiếu thư viện.
- **Lệnh thực thi**:
  ```powershell
  python -m PyInstaller slideshow.spec
  ```
- **Kiểm tra tệp đầu ra**:
  - Tệp `dist/Slideshow.exe` được sinh ra.
  - Chạy `dist/Slideshow.exe`, kiểm tra ứng dụng khởi chạy bình thường mà không mở cửa sổ console đen (`--noconsole`).

