# Tasks: Tái Cấu Trúc Dự Án Theo Clean Architecture

**Input**: Design documents from `specs/001-clean-architecture-refactor/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)

**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/`

**Organization**: Các tác vụ được phân bổ tuần tự theo các tầng Clean Architecture và ánh xạ tới từng User Story để đảm bảo tính độc lập và khả năng kiểm thử liên tục.

## Format: `[TaskID] [P?] [Story?] Description with file path`

- **[P]**: Có thể chạy song song (các tệp độc lập, không phụ thuộc nhau)
- **[Story]**: Gắn nhãn User Story (`[US1]`, `[US2]`, `[US3]`, `[US4]`)
- Mô tả tác vụ luôn chỉ định đường dẫn tệp cụ thể và trích dẫn ràng buộc xác thực rõ ràng

---

## Phase 1: Setup (Khởi Tạo Cấu Trúc Thư Mục Clean Architecture)

**Purpose**: Thiết lập bộ khung thư mục phân tầng Clean Architecture trong `src/`

- [X] T001 Tạo cấu trúc các thư mục phân tầng Clean Architecture gồm `src/domain/`, `src/application/`, `src/infrastructure/`, `src/presentation/views/`
- [X] T002 [P] Khởi tạo các tệp gói package `__init__.py` cho `src/domain/__init__.py`, `src/application/__init__.py`, `src/infrastructure/__init__.py`, `src/presentation/__init__.py` và `src/presentation/views/__init__.py`

---

## Phase 2: Foundational (Các Thành Phần Nền Tảng Cốt Lõi)

**Purpose**: Các thực thể dữ liệu, interfaces và tiện ích dùng chung chặn trước mọi User Story

- [X] T003 [P] Định nghĩa các Domain Models bằng dataclasses trong `src/domain/models.py`: `ImageItem` (ràng buộc: `path` không rỗng, đuôi mở rộng hợp lệ trong `('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')`), `Playlist` (ràng buộc: quản lý `current_index`, `is_random`, ngăn xếp `history`), `ViewerSettings` (ràng buộc: `interval_ms >= 1000`, `bg_color` hex hợp lệ, `window_geometry` mảng 4 số nguyên `[x, y, w, h]` với `w >= 400, h >= 300`)
- [X] T004 [P] Định nghĩa các Ports giao tiếp trừu tượng (`ImageRepositoryPort`, `SettingsRepositoryPort`, `SystemIntegrationPort`) bằng `typing.Protocol` trong `src/domain/ports.py`
- [X] T005 [P] Triển khai thuật toán tách chuỗi sắp xếp tên tự nhiên Windows (`_natural_sort_key`) khớp với Windows Explorer trong `src/application/sorting.py`
- [X] T006 [P] Triển khai tiện ích phân giải đường dẫn tài nguyên `get_resource_path()` cho cả chế độ script dev và đóng gói PyInstaller frozen exe trong `src/infrastructure/path_utils.py`

**Checkpoint**: Nền tảng Core Domain và Ports đã sẵn sàng, có thể kiểm thử độc lập không phụ thuộc Qt.

---

## Phase 3: User Story 2 (P1) - Tách Biệt Tầng Nghiệp Vụ (Application Use Cases)

**Goal**: Triển khai các Use Cases nghiệp vụ thuần túy, hoàn toàn độc lập khỏi `PyQt6`

- [X] T007 [P] [US2] Triển khai `LoadImagesUseCase` quét và nạp ảnh từ thư mục có hỗ trợ mở ảnh từ `start_file` và tự động sắp xếp natural sort trong `src/application/use_cases.py`
- [X] T008 [P] [US2] Triển khai `NavigatePlaylistUseCase` xử lý duyệt ảnh tuần tự và ngẫu nhiên có lưu lịch sử để lùi ảnh chính xác trong `src/application/use_cases.py`
- [X] T009 [P] [US2] Triển khai `DeleteImageUseCase` điều phối xóa ảnh và cập nhật chỉ mục playlist trong `src/application/use_cases.py`
- [X] T010 [P] [US2] Triển khai `ManageFavoritesUseCase` thêm/bớt ảnh khỏi danh sách yêu thích trong `src/application/use_cases.py`
- [X] T011 [P] [US2] Triển khai `ManageSettingsUseCase` lưu/tải và cập nhật thiết lập hiển thị trong `src/application/use_cases.py`
- [X] T012 [US2] Chạy kịch bản kiểm thử xác thực độc lập cho toàn bộ Use Cases và Domain Models không cần Qt theo hướng dẫn tại `specs/001-clean-architecture-refactor/quickstart.md`

**Checkpoint**: Tầng Domain và Application hoàn thành 100%, độc lập tuyệt đối với UI.

---

## Phase 4: User Story 3 (P2) - Tầng Infrastructure & Hợp Nhất Cấu Hình

**Goal**: Đóng gói các adapter giao tiếp hệ thống, loại bỏ code dư thừa và hợp nhất cấu hình về `settings.json`

- [X] T013 [P] [US3] Triển khai `JsonSettingsRepository` đọc/ghi `settings.json` an toàn với cơ chế fallback mặc định (`interval_ms: 3000, bg_color: "#000000", favorites: []`) trong `src/infrastructure/json_settings_repo.py`
- [X] T014 [P] [US3] Triển khai `LocalImageRepository` sử dụng `glob` quét tệp ảnh theo danh sách đuôi mở rộng và `send2trash` chuyển ảnh vào Recycle Bin an toàn trong `src/infrastructure/local_image_repo.py`
- [X] T015 [P] [US3] Triển khai `WindowsSystemAdapter` tích hợp `winreg` đăng ký Open With (`Software\Classes`), `ctypes` gán AppUserModelID và lệnh mở Explorer trong `src/infrastructure/windows_system_adapter.py`
- [X] T016 [US3] Xóa bỏ tệp dư thừa không sử dụng `src/config_manager.py` (và `config.json` nếu có) theo quyết định Option A trong `src/config_manager.py`
- [X] T017 [US3] Tạo shim mỏng `src/config.py` chuyển tiếp các lời gọi `load_settings()` và `save_settings()` sang `JsonSettingsRepository` để tương thích ngược trong `src/config.py`

**Checkpoint**: Tầng Infrastructure hoàn tất, toàn bộ cấu hình hợp nhất vào `settings.json`.

---

## Phase 5: User Story 1 (P1) - Tầng Presentation & Tích Hợp Zero-Regression

**Goal**: Kết nối các thành phần giao diện PyQt6 với Use Cases qua Presenter, đảm bảo giữ nguyên 100% chức năng

- [X] T018 [US1] Triển khai `ViewerPresenter` làm cầu nối điều phối giữa các Use Cases và `PhotoViewerViewContract` trong `src/presentation/presenter.py`
- [X] T019 [P] [US1] Di chuyển và tái cấu trúc `ControlPanel` widget sang tầng Presentation trong `src/presentation/views/control_panel.py`
- [X] T020 [P] [US1] Di chuyển và tái cấu trúc `CustomSplashScreen` sang tầng Presentation, giữ logic đa màn hình trong `src/presentation/views/splash_screen.py`
- [X] T021 [P] [US1] Di chuyển và tái cấu trúc `SettingsDialog` sang tầng Presentation, kết nối với `ManageSettingsUseCase` trong `src/presentation/views/settings_dialog.py`
- [X] T022 [P] [US1] Di chuyển và tái cấu trúc `FavoritesWindow` sang tầng Presentation trong `src/presentation/views/favorites_window.py`
- [X] T023 [US1] Tái cấu trúc cửa sổ chính `PhotoViewerWindow` trong `src/presentation/views/viewer_window.py`, tách logic nghiệp vụ sang `ViewerPresenter`, giữ nguyên giao diện Dark Theme, phím tắt, canvas `QGraphicsView` zoom/pan
- [X] T024 [US1] Cập nhật Composition Root `main.py` để khởi tạo Dependency Injection (Repositories, Use Cases, Presenter, Views) và xử lý tham số CLI `sys.argv[1]`
- [X] T025 [US1] Dọn dẹp các tệp mã nguồn cũ ở thư mục gốc `src/` (`src/image_loader.py`, `src/control_panel.py`, `src/splash_screen.py`, `src/settings_dialog.py`, `src/favorites_window.py`, `src/viewer_window.py`) sau khi đã chuyển sang các tầng mới

**Checkpoint**: Ứng dụng chạy mượt mà từ mã nguồn `python main.py`, giữ nguyên toàn bộ giao diện và phím tắt.

---

## Phase 6: User Story 4 (P3) - Cập Nhật Hiến Pháp Dự Án (`constitution.md`)

**Goal**: Viết lại file `.specify/memory/constitution.md` để quy định luật lệ Clean Architecture cho dự án

- [X] T026 [US4] Cập nhật `.specify/memory/constitution.md` bổ sung nguyên tắc phân tầng Clean Architecture, ranh giới phụ thuộc (Dependency Rule) và cấu trúc thư mục mới
- [X] T027 [US4] Cập nhật Sync Impact Report và nâng số hiệu phiên bản hiến pháp trong `.specify/memory/constitution.md`

**Checkpoint**: Hiến pháp dự án được đồng bộ hoàn hảo với hiện trạng kiến trúc mới.

---

## Phase 7: Polish & Đóng Gói PyInstaller

**Purpose**: Hoàn thiện đóng gói, kiểm thử end-to-end và tối ưu hóa

- [X] T028 [P] Cập nhật tệp kịch bản đóng gói PyInstaller `slideshow.spec` phù hợp với cấu trúc phân tầng mới trong `slideshow.spec`
- [X] T029 Chạy kiểm thử xác thực theo 4 kịch bản trong `specs/001-clean-architecture-refactor/quickstart.md`
- [X] T030 Thực hiện build thử nghiệm đóng gói `python -m PyInstaller slideshow.spec` và xác nhận chạy thành công tệp `dist/Slideshow.exe`

---

## Dependencies & Execution Order

### Phase Dependencies
1. **Phase 1 (Setup)**: Có thể bắt đầu ngay lập tức.
2. **Phase 2 (Foundational)**: Phụ thuộc vào Phase 1; chặn toàn bộ các User Stories.
3. **Phase 3 (User Story 2 - Core Use Cases)**: Phụ thuộc vào Phase 2.
4. **Phase 4 (User Story 3 - Infrastructure)**: Có thể làm song song hoặc ngay sau Phase 3.
5. **Phase 5 (User Story 1 - Presentation & UI)**: Phụ thuộc vào Phase 3 và Phase 4.
6. **Phase 6 (User Story 4 - Constitution)**: Phụ thuộc vào việc hoàn thiện cấu trúc mã nguồn.
7. **Phase 7 (Polish & Build)**: Thực thi cuối cùng sau khi hoàn tất toàn bộ các pha trước.

### Parallel Opportunities
- T003, T004, T005, T006 có thể triển khai song song trong Phase 2.
- T007, T008, T009, T010, T011 có thể triển khai song song trong Phase 3.
- T013, T014, T015 có thể triển khai song song trong Phase 4.
- T019, T020, T021, T022 có thể di chuyển và tái cấu trúc song song trong Phase 5.
