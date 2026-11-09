<!--
Sync Impact Report:
- Version change: v1.0.0 -> v1.1.0
- List of modified principles:
  - PRINCIPLE_1: Nâng cấp thành "I. Kiến Trúc Clean Architecture & Quy Tắc Phụ Thuộc (Clean Architecture & Dependency Rule)" - Quy định 4 tầng rõ rệt (Domain, Application, Infrastructure, Presentation) và cấm tuyệt đối import PyQt6 ở tầng Domain và Application.
  - PRINCIPLE_3: Bổ sung quy định hợp nhất cấu hình về duy nhất settings.json qua JsonSettingsRepository.
- Added sections:
  - Cập nhật sơ đồ cấu trúc thư mục mới trong Technical Stack & Architectural Constraints.
- Removed sections: Không có.
- Follow-up TODOs: Không có.
-->

# PhotoViewerApp Constitution

## Core Principles

### I. Kiến Trúc Clean Architecture & Quy Tắc Phụ Thuộc (Clean Architecture & Dependency Rule)
Mọi chức năng mới MUST tuân thủ nghiêm ngặt mô hình Clean Architecture 4 tầng với nguyên tắc phụ thuộc một chiều (Dependencies point inward):
- **Tầng 1 - Domain (`src/domain/`)**: Chứa các thực thể cốt lõi (`ImageItem`, `Playlist`, `ViewerSettings`) và các Ports giao tiếp trừu tượng (`ports.py`). Tầng Domain MUST là Python thuần túy, TUYỆT ĐỐI KHÔNG chứa bất kỳ lệnh import nào từ framework giao diện (`PyQt6`) hoặc các thư viện nền tảng ngoài Python Standard Library.
- **Tầng 2 - Application (`src/application/`)**: Chứa các kịch bản nghiệp vụ (Use Cases: `LoadImagesUseCase`, `NavigatePlaylistUseCase`, `DeleteImageUseCase`, `ManageFavoritesUseCase`, `ManageSettingsUseCase`) và thuật toán nghiệp vụ (`sorting.py`). Tầng Application chỉ phụ thuộc vào Domain, KHÔNG phụ thuộc vào tầng Presentation hay Infrastructure.
- **Tầng 3 - Infrastructure (`src/infrastructure/`)**: Chứa các Adapters cụ thể triển khai các Ports trừu tượng: đọc/ghi cấu hình JSON (`json_settings_repo.py`), quét tệp và chuyển vào thùng rác (`local_image_repo.py`), tích hợp Windows Registry và AppUserModelID (`windows_system_adapter.py`), tiện ích đường dẫn (`path_utils.py`).
- **Tầng 4 - Presentation (`src/presentation/`)**: Chứa Presenter điều phối (`presenter.py`) và toàn bộ giao diện người dùng PyQt6 (`views/`). Presenter giao tiếp với Use Cases để lấy dữ liệu thuần túy và đẩy sang View.
- **Composition Root (`main.py`)**: Là điểm duy nhất khởi tạo, cấu hình Dependency Injection và chạy vòng lặp sự kiện `app.exec()`. Không được nhúng logic nghiệp vụ xử lý ảnh vào `main.py`.
- Rationale: Giúp việc kiểm thử độc lập logic xem ảnh không cần khởi động Qt, dễ dàng thay thế giao diện hoặc lưu trữ mà không làm ảnh hưởng đến lõi nghiệp vụ.

### II. Chuẩn Giao Diện PyQt6 & Trải Nghiệm Windows Native (Native UI/UX & Dark Theme)
Toàn bộ giao diện người dùng MUST được xây dựng trên nền tảng PyQt6 với ngôn ngữ thiết kế đồng nhất:
- Ứng dụng áp dụng bảng màu Dark Mode tương phản cao làm mặc định; màu sắc điểm nhấn chính (accent color) là tông Cyan/Teal (`#00adb5`), nút cảnh báo hoặc yêu thích dùng màu đỏ (`#d9534f`).
- Bố cục thanh công cụ và các nút điều hướng nổi (overlay buttons) MUST sử dụng nền mờ bán trong suốt (semi-transparent), bo tròn góc hiện đại, không cản trở vùng hiển thị nội dung ảnh.
- Canvas trình chiếu MUST dựa trên `QGraphicsView` và `QGraphicsScene`, đảm bảo hỗ trợ mượt mà các thao tác zoom vô cấp, pan (ScrollHandDrag) và giữ nguyên tỉ lệ khung hình (KeepAspectRatio).
- Cửa sổ ứng dụng MUST hỗ trợ đa màn hình (multi-monitor awareness), tự động lưu và khôi phục tọa độ hình học (`window_geometry`), trạng thái toàn màn hình (`is_fullscreen`) và phóng to (`is_maximized`).
- Rationale: Đảm bảo giao diện hiện đại, chuyên nghiệp, phản hồi nhanh và tạo trải nghiệm xem ảnh tự nhiên, liền mạch cho người dùng hệ điều hành Windows.

### III. An Toàn Dữ Liệu & Khả Năng Phục Hồi (Safe Operations & Data Resilience)
Mọi thao tác can thiệp vào tệp tin và cấu hình hệ thống MUST đặt an toàn dữ liệu của người dùng lên hàng đầu:
- Khi người dùng chọn xóa ảnh, ứng dụng MUST sử dụng cơ chế `send2trash` để chuyển tệp vào Thùng rác (Recycle Bin) của Windows, TUYỆT ĐỐI KHÔNG xóa vĩnh viễn (`os.remove`) nếu không có chỉ định bắt buộc kèm xác nhận nhiều lớp.
- Thao tác xóa hoặc thay đổi dữ liệu MUST luôn hiển thị hộp thoại xác nhận (`QMessageBox.question`).
- Quá trình đọc/ghi cấu hình MUST hợp nhất về duy nhất tệp `settings.json` thông qua `JsonSettingsRepository`, có cơ chế phòng vệ lỗi (fallback defaults), tự động khôi phục cấu hình mặc định an toàn khi tệp bị hỏng hoặc thiếu trường dữ liệu, không được làm crash ứng dụng khi khởi động.
- Trình nạp ảnh MUST xử lý ngoại lệ khi tệp ảnh bị lỗi, ảnh định dạng lạ hoặc bị xóa bởi tiến trình khác trong lúc đang trình chiếu mà không làm gián đoạn vòng lặp hiển thị.
- Rationale: Bảo vệ dữ liệu cá nhân của người dùng khỏi việc mất mát ngẫu nhiên và nâng cao độ tin cậy của phần mềm.

### IV. Tích Hợp Hệ Điều Hành & Thao Tác Trực Quan (System Integration & Ergonomics)
Ứng dụng MUST hòa nhập chặt chẽ với hệ sinh thái Windows để đem lại trải nghiệm tiện dụng tối đa:
- Hỗ trợ đầy đủ tham số dòng lệnh (`sys.argv[1]`) để người dùng có thể nhấp đúp hoặc chọn "Open with" trực tiếp từ Windows File Explorer; tự động định vị đúng ảnh được mở trong danh sách thư mục.
- Tự động duy trì đăng ký giao thức mở tệp qua Windows Registry (`HKCU\Software\Classes`) cho các định dạng ảnh phổ biến (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`).
- Đặt `AppUserModelID` qua `ctypes` để Windows Taskbar hiển thị chính xác biểu tượng ứng dụng riêng biệt thay vì icon Python mặc định.
- Danh sách tệp ảnh MUST được sắp xếp theo quy tắc số tự nhiên (Windows Natural Sort: ví dụ `2.jpg` đứng trước `10.jpg`) tương đồng với hành vi của File Explorer.
- Hệ thống phím tắt MUST bao phủ các thao tác cốt lõi: Mũi tên Trái/Phải (Duyệt ảnh), Phím Cách (Tạm dừng/Trình chiếu), `F11` hoặc Nhấp đúp chuột (Bật/Tắt Fullscreen), `Esc` (Thoát Fullscreen), `H` (Ẩn/Hiện bảng điều khiển).
- Rationale: Giúp ứng dụng hoạt động tương thích hoàn toàn như một phần mềm xem ảnh native của Windows, giảm thiểu rào cản thao tác cho người dùng.

### V. Tính Độc Lập & Tương Thích Đóng Gói EXE (Self-Contained & PyInstaller Readiness)
Mọi sự thay đổi về mã nguồn và phụ thuộc MUST đảm bảo ứng dụng có thể đóng gói thành một tệp thực thi duy nhất:
- Dự án ưu tiên sử dụng thư viện chuẩn của Python và PyQt6; KHÔNG tự ý đưa vào các thư viện bên ngoài cồng kềnh hoặc phụ thuộc vào C/C++ runtime phức tạp nếu chưa có phân tích và phê duyệt kiến trúc.
- Mã nguồn MUST sử dụng `path_utils.py` để xác định chính xác đường dẫn tài nguyên (icon, tệp cấu hình, file thực thi) ở cả hai chế độ: chạy qua mã nguồn `python main.py` và chạy qua tệp đóng gói `Slideshow.exe`.
- Cấu hình đóng gói `slideshow.spec` MUST được cập nhật đồng bộ mỗi khi phát sinh thêm tài nguyên tĩnh (`datas`), thư viện ẩn (`hiddenimports`) hoặc tệp nhị phân (`binaries`).
- Rationale: Đảm bảo sản phẩm cuối cùng luôn sẵn sàng phân phối cho người dùng cuối trên Windows dưới dạng một tệp thực thi di động (portable executable) mà không yêu cầu cài đặt Python hay môi trường phức tạp.

## Technical Stack & Architectural Constraints

### 1. Ngôn Ngữ & Môi Trường Runtime
- **Ngôn ngữ**: Python 3 (khuyến nghị Python 3.10 - 3.12/3.14).
- **Hệ điều hành mục tiêu**: Microsoft Windows (Windows 10, Windows 11).
- **Mã hóa ký tự**: Toàn bộ tệp mã nguồn và tệp cấu hình MUST sử dụng mã hóa UTF-8 chuẩn.

### 2. Danh Mục Thư Viện Chính Thức
- **PyQt6 (`>= 6.4.0`)**: Thư viện GUI cốt lõi quản lý Widgets, GraphicsScene, Event Filters, Animations, Shortcuts.
- **send2trash (`>= 1.8.0`)**: Thư viện đưa tệp vào Windows Recycle Bin an toàn.
- **PyInstaller (`>= 5.0`)**: Công cụ đóng gói ứng dụng thành `.exe` chạy độc lập với cờ `--noconsole` và `--onefile`.
- **Thư viện chuẩn (Standard Library)**: `os`, `sys`, `glob`, `re`, `random`, `json`, `time`, `winreg`, `ctypes`, `dataclasses`, `typing`.

### 3. Cấu Trúc Thư Mục Clean Architecture Chuẩn
```text
src/
├── domain/                      # Tầng 1: Models & Ports trừu tượng (0 dependency)
│   ├── models.py
│   └── ports.py
├── application/                 # Tầng 2: Use Cases & Natural Sort
│   ├── use_cases.py
│   └── sorting.py
├── infrastructure/              # Tầng 3: Repositories & Windows OS Adapters
│   ├── json_settings_repo.py
│   ├── local_image_repo.py
│   ├── windows_system_adapter.py
│   └── path_utils.py
├── presentation/                # Tầng 4: Presenter & Views PyQt6
│   ├── presenter.py
│   └── views/
│       ├── viewer_window.py
│       ├── control_panel.py
│       ├── splash_screen.py
│       ├── settings_dialog.py
│       └── favorites_window.py
├── assets/
│   └── app_icon.ico
├── config.py                    # Shim tương thích ngược
└── __init__.py

main.py                          # Composition Root: Dependency Injection & App Start
slideshow.spec                   # Kịch bản đóng gói PyInstaller
settings.json                    # Cấu hình người dùng duy nhất
```

## Development Workflow & Quality Gates

### 1. Quy Trình Phát Triển Tính Năng (Spec Kit Flow)
Mọi thay đổi lớn hoặc tính năng mới MUST tuân thủ quy trình chuẩn:
1. **Đặc tả yêu cầu (`/speckit-specify`)**: Xác định mục tiêu, kịch bản sử dụng và tiêu chí chấp nhận.
2. **Làm rõ & Phân tích (`/speckit-clarify`, `/speckit-plan`)**: Thiết kế kiến trúc, đánh giá ảnh hưởng đến UI/UX và cơ chế lưu trữ.
3. **Phân rã tác vụ (`/speckit-tasks`)**: Lập danh sách các tác vụ có thứ tự phụ thuộc rõ ràng.
4. **Kiểm tra chéo (`/speckit-analyze`)**: Đảm bảo tính nhất quán giữa các tài liệu.
5. **Triển khai (`/speckit-implement`)**: Viết code, tự kiểm tra hồi quy và kiểm tra khả năng đóng gói.

### 2. Tiêu Chuẩn Chất Lượng Code (Quality Gates)
- **Chuẩn cú pháp**: Tuân thủ hướng dẫn định dạng PEP 8 cho mã nguồn Python; đặt tên biến, hàm theo phong cách `snake_case`, tên lớp theo `CamelCase`.
- **Ranh giới Clean Architecture**: Không để lọt bất kỳ import nào từ `PyQt6` vào `domain/` hay `application/`.
- **Xử lý tài nguyên UI**: Tất cả các timer (`QTimer`) và animation (`QPropertyAnimation`) MUST được quản lý dừng/chạy an toàn khi đóng cửa sổ hoặc mở dialog phụ nhằm tránh rò rỉ bộ nhớ hoặc lỗi vẽ khung hình.
- **Kiểm tra đóng gói**: Sau mỗi chu kỳ tính năng quan trọng, mã nguồn MUST được kiểm tra chạy trực tiếp và xác nhận lệnh `pyinstaller slideshow.spec` hoàn thành không lỗi.

## Governance

Hiến pháp này là bộ quy tắc kỹ thuật cao nhất của dự án PhotoViewerApp. Mọi đề xuất kiến trúc, mã nguồn đóng góp và quy trình phát triển bắt buộc phải tuân thủ nghiêm ngặt các nguyên tắc nêu trên.

- **Thẩm quyền sửa đổi**: Mọi sửa đổi nguyên tắc trong hiến pháp phải được ghi nhận rõ lý do, đánh giá mức độ tương thích ngược và cập nhật tài liệu liên quan.
- **Quy tắc phiên bản hiến pháp (Semantic Versioning)**:
  - Tăng số hiệu **MAJOR** khi có sự thay đổi triết lý cốt lõi, loại bỏ nguyên tắc hoặc tái cấu trúc toàn diện kiến trúc công nghệ (ví dụ chuyển từ PyQt6 sang framework khác).
  - Tăng số hiệu **MINOR** khi bổ sung nguyên tắc mới, mở rộng quy định kỹ thuật hoặc bổ sung chuẩn phát triển tính năng mới (ví dụ chuẩn hóa Clean Architecture 4 tầng).
  - Tăng số hiệu **PATCH** khi chỉnh sửa câu từ, giải thích chi tiết hơn hoặc sửa các lỗi chính tả, định dạng nhỏ.
- **Giám sát tuân thủ**: Mọi bước phát triển tiếp theo thông qua Spec Kit MUST đối chiếu với các nguyên tắc trong Hiến pháp này trước khi thực thi.

**Version**: 1.1.0 | **Ratified**: 2026-11-09 | **Last Amended**: 2026-11-09
