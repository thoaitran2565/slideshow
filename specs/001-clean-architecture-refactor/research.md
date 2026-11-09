# Research: Tái Cấu Trúc Theo Clean Architecture

**Feature**: `001-clean-architecture-refactor`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Nghiên cứu Mô hình Clean Architecture cho Ứng dụng Desktop Python (PyQt6)

### Decision
Áp dụng mô hình **Clean Architecture 4 tầng** tiêu chuẩn cho ứng dụng desktop Python:
1. **Domain Layer (`src/domain/`)**: Thuần túy Python (Plain Old Python Objects / Dataclasses & Protocols). Không phụ thuộc bất kỳ thư viện thứ ba hay Qt nào. Chứa Entities (`ImageItem`, `ViewerSettings`, `Playlist`) và Ports/Interfaces (`ImageRepository`, `SettingsRepository`, `SystemIntegrationPort`).
2. **Application Layer (`src/application/`)**: Chứa Use Cases thực thi các kịch bản người dùng (`LoadImagesUseCase`, `NavigateImagesUseCase`, `ToggleSlideshowUseCase`, `ManageFavoritesUseCase`, `DeleteImageUseCase`, `ManageSettingsUseCase`). Tương tác với Domain qua Ports.
3. **Infrastructure Layer (`src/infrastructure/`)**: Triển khai các Ports cụ thể:
   - `JsonSettingsRepository`: Đọc/ghi cấu hình từ `settings.json` với fallback mặc định an toàn.
   - `LocalImageRepository`: Quét ảnh từ đĩa cứng theo định dạng, xóa ảnh an toàn bằng `send2trash`.
   - `WindowsSystemAdapter`: Đăng ký Windows Registry (`winreg`), gán AppUserModelID (`ctypes`), mở tệp trong Explorer.
4. **Presentation Layer (`src/presentation/`)**:
   - `views/`: Các cửa sổ và widget PyQt6 (`PhotoViewerWindow`, `ControlPanel`, `CustomSplashScreen`, `SettingsDialog`, `FavoritesWindow`).
   - `controllers/` hoặc `presenters/`: Điều phối sự kiện người dùng từ UI, gọi Use Case và chuyển dữ liệu trở lại UI.
5. **Composition Root (`main.py`)**: Nơi duy nhất khởi tạo (Instantiate) và nối ghép các phụ thuộc (Dependency Injection), sau đó chạy `app.exec()`.

### Rationale
- Tách biệt hoàn toàn logic nghiệp vụ khỏi giao diện PyQt6, cho phép kiểm thử logic duyệt ảnh, sắp xếp, quản lý lịch sử mà không cần chạy vòng lặp Qt (`QApplication`).
- Giữ vững Nguyên tắc I và II trong Hiến pháp dự án.
- Giúp việc mở rộng sau này (ví dụ thêm backend quét ảnh đệ quy, đồng bộ đám mây, hay thay đổi giao diện) không ảnh hưởng tới logic cốt lõi.

### Alternatives Considered
- *Kiến trúc MVC truyền thống trong PyQt*: Trộn lẫn Controller với Qt Signals trực tiếp trong QMainWindow. Bị bác bỏ vì dễ dẫn tới "God Object" (`PhotoViewerWindow` nặng hơn 500 dòng làm mọi thứ từ nạp ảnh, Registry, animation đến quản lý cấu hình).
- *Kiến trúc MVVM với QObject Property Binding*: Đòi hỏi biến toàn bộ Domain Entities thành `QObject`, làm logic nghiệp vụ dính chặt vào thư viện Qt, vi phạm nguyên tắc độc lập của Clean Architecture.

---

## 2. Xử Lý Tương Thích Ngược & An Toàn Dữ Liệu (Zero-Regression)

### Decision
- Tiếp tục sử dụng tệp `settings.json` làm nguồn cấu hình chính thức duy nhất.
- Hợp nhất và loại bỏ hoàn toàn tệp `config_manager.py` (vốn định nghĩa `config.json` song song nhưng không dùng đầy đủ).
- Bảo lưu 100% các phím tắt, thao tác chuột (click đơn/click đúp phân biệt timer, kéo chuột ScrollHandDrag khi zoom, con lăn zoom).
- Duy trì thuật toán sắp xếp tự nhiên `_natural_sort_key` trong Domain/Use Case để đảm bảo thứ tự ảnh khớp chính xác với Windows File Explorer.

### Rationale
- Đảm bảo người dùng cuối không nhận thấy bất kỳ sự xáo trộn nào về dữ liệu cấu hình hoặc thói quen sử dụng sau khi nâng cấp.
- Loại bỏ nợ kỹ thuật tồn đọng trong mã nguồn cũ.

---

## 3. Khả Năng Đóng Gói PyInstaller

### Decision
- Giữ cấu trúc import tuyệt đối trong package `src` (ví dụ: `from src.domain.models import ImageItem`).
- Cập nhật tệp `slideshow.spec` để đảm bảo `pathex` và phân tích module tự động phát hiện toàn bộ các tầng mới mà không cần thêm cấu hình phức tạp.
- Sử dụng hàm tiện ích xác định đường dẫn chạy (frozen executable vs script dev) đặt trong `src/infrastructure/path_utils.py`.

### Rationale
- Đảm bảo quá trình build `python -m PyInstaller slideshow.spec` sinh ra tệp `dist/Slideshow.exe` hoạt động hoàn hảo trên mọi máy tính Windows mà không cần cài đặt Python.

