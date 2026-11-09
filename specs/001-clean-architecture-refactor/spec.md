# Feature Specification: Tái Cấu Trúc Dự Án Theo Clean Architecture (Clean Architecture Refactor)

**Feature Branch**: `001-clean-architecture-refactor`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "Xây dựng lại toàn bộ cấu trúc dự án - sử dụng kiến trúc clean architecture - Chia tách code gọn gàng và phân tách rõ code ui và logic - Viết lại file constitution.md sau khi điều chỉnh xong kiến trúc dự án"

## Clarifications

### Session 2026-11-09
- Q: Khi tái cấu trúc sang Clean Architecture, chúng ta nên xử lý các tệp cấu hình cũ (`src/config_manager.py` và `src/config.py`) như thế nào? → A: Option A (Xóa bỏ hoàn toàn `config_manager.py` tệp thừa không sử dụng, chuyển đổi `config.py` thành `JsonSettingsRepository` chuẩn Clean Architecture trong tầng Infrastructure, chỉ sử dụng duy nhất tệp `settings.json` làm nguồn chân lý cấu hình, giữ một shim `config.py` mỏng tương thích ngược nếu cần).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trải Nghiệm Xem Ảnh & Trình Chiếu Không Đổi (Zero Regression) (Priority: P1)

Là một người dùng xem ảnh trên Windows, tôi muốn tiếp tục sử dụng toàn bộ tính năng quen thuộc (trình chiếu tự động, chuyển ảnh tới/lùi, chuyển chế độ ngẫu nhiên, đổi tốc độ, phóng to/thu nhỏ, kéo rê ảnh, toàn màn hình, yêu thích, xóa ảnh vào thùng rác) một cách mượt mà và chính xác như trước đây, để công việc xem ảnh của tôi không bị gián đoạn hay sai lệch hành vi sau khi tái cấu trúc mã nguồn.

**Why this priority**: Đảm bảo an toàn tuyệt đối cho người dùng cuối. Việc tái cấu trúc kiến trúc phần mềm phải giữ nguyên 100% chức năng và trải nghiệm người dùng hiện có.

**Independent Test**: Khởi chạy ứng dụng từ mã nguồn hoặc dòng lệnh với ảnh mẫu, thực hiện tất cả các thao tác (Play/Pause, Prev/Next, Zoom, Pan, Fullscreen, Favorite, Delete) và xác nhận hoạt động trơn tru không lỗi.

**Acceptance Scenarios**:

1. **Given** ứng dụng đang mở một thư mục ảnh, **When** người dùng duyệt ảnh bằng phím tắt hoặc nút bấm, **Then** ảnh mới được nạp và hiển thị ngay lập tức với hiệu ứng chuyển cảnh mượt mà.
2. **Given** ứng dụng đang ở chế độ trình chiếu tự động, **When** hết khoảng thời gian đặt trước (`interval_ms`), **Then** ứng dụng tự động chuyển sang ảnh tiếp theo (hoặc ngẫu nhiên nếu bật chế độ Random).
3. **Given** người dùng chọn xóa ảnh hiện tại, **When** người dùng xác nhận trong hộp thoại, **Then** ảnh được đưa vào Thùng rác Windows an toàn và ảnh kế tiếp lập tức được hiển thị.

---

### User Story 2 - Phân Tách Tuyệt Đối Tầng Nghiệp Vụ (Core Domain/Logic) và Giao Diện (UI) (Priority: P1)

Là một lập trình viên duy trì dự án, tôi muốn mã nguồn nghiệp vụ (quản lý danh sách ảnh, logic sắp xếp tên tự nhiên, bộ đếm chỉ số, trạng thái trình chiếu, quản lý cấu hình) được cô lập hoàn toàn khỏi giao diện người dùng (PyQt6 widgets), để tôi có thể dễ dàng viết kiểm thử tự động (Unit Test), bảo trì và nâng cấp mà không sợ ảnh hưởng đến tầng giao diện.

**Why this priority**: Đây là mục tiêu cốt lõi của kiến trúc Clean Architecture: tách biệt ranh giới (boundaries), đảm bảo logic cốt lõi không phụ thuộc vào bất kỳ framework hiển thị nào.

**Independent Test**: Chạy kiểm thử tự động hoặc kiểm tra import cho toàn bộ tầng Domain và Use Cases để xác nhận không có bất kỳ import nào từ `PyQt6.QtWidgets` hay `PyQt6.QtGui`.

**Acceptance Scenarios**:

1. **Given** tầng nghiệp vụ xử lý danh sách ảnh (`ImagePlaylist` / `LoadImagesUseCase`), **When** thực thi quét thư mục và sắp xếp ảnh theo thứ tự tự nhiên của Windows, **Then** logic hoạt động độc lập và trả về dữ liệu thuần túy (Domain Entities/Value Objects) mà không cần khởi tạo Qt Application.
2. **Given** tầng giao diện PyQt6 (`PhotoViewerWindow`, `ControlPanel`), **When** người dùng tương tác (click nút, bấm phím), **Then** giao diện chỉ đóng vai trò gửi sự kiện/yêu cầu tới Presentation/Controller/Use Case và cập nhật lại hiển thị dựa trên phản hồi dữ liệu.

---

### User Story 3 - Hợp Nhất & Tách Biệt Cấu Hình và Giao Tiếp Hệ Thống (Priority: P2)

Là một lập trình viên và người dùng, tôi muốn việc lưu trữ cài đặt (`settings.json`), giao tiếp với Windows Registry và thao tác xóa tệp (`send2trash`) được đóng gói qua các Adapter/Repository chuyên biệt, đồng thời loại bỏ các tệp cấu hình dư thừa hoặc chồng chéo (`config_manager.py` vs `config.py`), để dữ liệu luôn nhất quán và an toàn.

**Why this priority**: Đảm bảo tính nhất quán của hệ thống lưu trữ, loại bỏ nợ kỹ thuật (technical debt) và bảo vệ an toàn tệp tin hệ thống.

**Independent Test**: Thay đổi thư mục ảnh, màu nền, tốc độ và danh sách yêu thích; đóng ứng dụng và mở lại để xác thực cấu hình được khôi phục chính xác từ một nguồn `settings.json` duy nhất.

**Acceptance Scenarios**:

1. **Given** người dùng thay đổi các thiết lập trong Settings Dialog, **When** lưu cài đặt, **Then** dữ liệu được ghi chuẩn xác vào `settings.json` thông qua Settings Repository mà không có xung đột từ các file cấu hình khác.
2. **Given** ứng dụng được khởi chạy với đối số dòng lệnh (`sys.argv[1]`), **When** mở ảnh qua tính năng "Open with" của Windows, **Then** Adapter xử lý CLI nhận diện đúng đường dẫn và nạp danh sách ảnh xung quanh tệp đó.

---

### User Story 4 - Cập Nhật Hiến Pháp Dự Án Phù Hợp Kiến Trúc Mới (Priority: P3)

Là thành viên phát triển dự án, tôi muốn file `constitution.md` được cập nhật đồng bộ sau khi hoàn thành tái cấu trúc, nhằm thiết lập các luật lệ và tiêu chuẩn bắt buộc cho kiến trúc Clean Architecture để các bước phát triển tính năng tiếp theo luôn tuân thủ.

**Why this priority**: Đảm bảo tính nhất quán lâu dài theo quy chuẩn quản trị dự án của Spec Kit.

**Independent Test**: Đọc và kiểm tra file `.specify/memory/constitution.md` để xác nhận các quy định về Clean Architecture, ranh giới tầng và tiêu chuẩn kiểm thử đã được cập nhật đầy đủ.

**Acceptance Scenarios**:

1. **Given** kiến trúc Clean Architecture đã được triển khai xong, **When** cập nhật `constitution.md`, **Then** hiến pháp phản ánh cấu trúc thư mục mới, nguyên tắc phụ thuộc (Dependency Rule) và tiêu chuẩn chất lượng mã nguồn mới.

---

### Edge Cases

- **Mở tệp ảnh từ đường dẫn mạng hoặc đường dẫn chứa ký tự tiếng Việt có dấu/khoảng trắng**: Hệ thống phải xử lý chuẩn hóa đường dẫn Unicode an toàn.
- **Tệp cấu hình `settings.json` bị trống hoặc định dạng JSON không hợp lệ**: Tầng Adapter cấu hình phải tự động nạp thiết lập mặc định an toàn và ghi đè lại file mà không gây dừng chương trình đột ngột.
- **Thư mục ảnh không chứa bất kỳ tệp ảnh hợp lệ nào**: Ứng dụng hiển thị thông báo trạng thái "Không có ảnh" trên giao diện và vô hiệu hóa các nút duyệt ảnh thay vì bị lỗi crash.
- **Đóng gói PyInstaller thành tệp thực thi duy nhất (`Slideshow.exe`)**: Cấu trúc module mới không làm sót hidden imports và nhận diện đúng các đường dẫn tài nguyên tĩnh (`app_icon.ico`).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Hệ thống MUST tổ chức mã nguồn theo 4 tầng của Clean Architecture:
  - **Domain**: Chứa các thực thể cốt lõi (`ImageItem`, `Playlist`, `ViewerConfig`) và các giao diện trừu tượng (Interfaces/Protocols), hoàn toàn độc lập với mọi thư viện ngoài.
  - **Application (Use Cases)**: Chứa các kịch bản nghiệp vụ độc lập (`LoadImagesUseCase`, `NavigateImageUseCase`, `ToggleSlideshowUseCase`, `ManageFavoritesUseCase`, `DeleteImageUseCase`).
  - **Adapters / Infrastructure**: Chứa các triển khai cụ thể cho việc đọc ghi cấu hình JSON, thao tác tệp tin (`send2trash`), đăng ký Windows Registry và đọc tham số hệ thống.
  - **Presentation / UI**: Chứa toàn bộ giao diện người dùng PyQt6 (`Views`, `Widgets`, `Dialogs`) và tầng điều phối giao diện (`Presenter`/`Controller`).
- **FR-002**: Tầng Domain và Application MUST NOT chứa bất kỳ lệnh import nào từ framework giao diện (`PyQt6`) hoặc các module nền tảng bên ngoài không thuộc Python Standard Library.
- **FR-003**: Ứng dụng MUST duy trì 100% các tính năng hiện có:
  - Trình chiếu ảnh tự động theo thời gian cấu hình tùy chỉnh (`interval_ms`).
  - Duyệt ảnh thủ công (tiếp theo, trước đó) bằng chuột và phím tắt (`Left`, `Right`, `Space`, `F11`, `Esc`, `H`).
  - Chế độ hiển thị ngẫu nhiên (Random) có ghi nhận lịch sử duyệt để lùi ảnh chính xác.
  - Thu phóng ảnh vô cấp (Zoom) bằng con lăn chuột và di chuyển ảnh (Pan) khi đang zoom.
  - Chế độ toàn màn hình (Fullscreen) mượt mà bằng phím `F11` hoặc nhấp đúp chuột.
  - Đổi màu nền hiển thị của canvas trình chiếu và lưu vào cấu hình.
  - Thêm/bớt ảnh vào danh sách Yêu thích (Favorites) và cửa sổ quản lý bộ sưu tập yêu thích.
  - Xóa ảnh vào Thùng rác Windows (`send2trash`) kèm hộp thoại xác nhận.
  - Sao chép đường dẫn ảnh vào Clipboard và mở vị trí ảnh trong File Explorer.
- **FR-004**: Hệ thống MUST loại bỏ hoàn toàn tệp cấu hình không dùng `config_manager.py` (và `config.json`), chuyển đổi logic `config.py` thành `JsonSettingsRepository` trong tầng Infrastructure và sử dụng duy nhất tệp `settings.json` làm nguồn chân lý cấu hình (Option A từ Clarifications).
- **FR-005**: Ứng dụng MUST xử lý được tham số dòng lệnh (`sys.argv[1]`) để hoạt động liền mạch với tính năng "Open with" của Windows Explorer.
- **FR-006**: Tự động duy trì việc đăng ký liên kết tệp trong Windows Registry (`HKCU\Software\Classes`) cho các định dạng ảnh `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`.
- **FR-007**: Tầng UI MUST phản hồi mượt mà, không xảy ra hiện tượng đóng băng (freezing) khi quét các thư mục chứa số lượng lớn ảnh.
- **FR-008**: Tệp kịch bản đóng gói PyInstaller (`slideshow.spec`) MUST được cập nhật tương thích hoàn toàn với cấu trúc thư mục mới, đảm bảo đóng gói thành công thành `Slideshow.exe`.
- **FR-009**: Sau khi tái cấu trúc hoàn tất, tài liệu Hiến pháp dự án (`.specify/memory/constitution.md`) MUST được viết lại để cập nhật toàn diện các quy chuẩn kiến trúc Clean Architecture.

### Key Entities *(include if feature involves data)*

- **ImageItem**: Đại diện cho một tệp ảnh trong hệ thống. Thuộc tính gồm: đường dẫn tuyệt đối (`path`), tên tệp (`filename`), kích thước, trạng thái yêu thích (`is_favorite`).
- **ImagePlaylist**: Đại diện cho tập hợp danh sách ảnh đang được trình chiếu. Quản lý danh sách các `ImageItem`, chỉ số hiện tại (`current_index`), chế độ ngẫu nhiên (`is_random`) và ngăn xếp lịch sử duyệt (`history`).
- **ViewerSettings**: Thực thể lưu trữ toàn bộ cấu hình ứng dụng: thư mục ảnh (`image_folder`), thời gian chuyển ảnh (`interval_ms`), màu nền (`bg_color`), danh sách đường dẫn yêu thích (`favorites`), trạng thái cửa sổ (`window_geometry`, `is_maximized`, `is_fullscreen`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% chức năng hiện có của ứng dụng hoạt động chính xác, không xuất hiện bất kỳ lỗi hồi quy (regression) nào trong các kịch bản người dùng.
- **SC-002**: 0 dòng mã thuộc framework giao diện (`PyQt6`) xuất hiện trong các thư mục thuộc tầng Domain và Application/Use Cases (tách biệt UI và logic đạt 100%).
- **SC-003**: Thời gian khởi động ứng dụng và thời gian phản hồi chuyển ảnh đạt dưới 100ms trong điều kiện sử dụng thông thường.
- **SC-004**: Ứng dụng đóng gói thành công bằng PyInstaller thành tệp thực thi độc lập `Slideshow.exe` và khởi chạy bình thường trên Windows mà không phụ thuộc vào môi trường phát triển.
- **SC-005**: File `constitution.md` được sửa đổi hoàn chỉnh phản ánh đúng cấu trúc Clean Architecture mới, đạt chuẩn đánh giá của Spec Kit.

## Assumptions

- Framework giao diện tiếp tục là `PyQt6` với phong cách Dark Mode và màu sắc hiện tại, không thay đổi trải nghiệm người dùng cuối.
- Cơ chế lưu trữ cấu hình tiếp tục dùng tệp `settings.json` đặt tại thư mục làm việc của ứng dụng để đảm bảo tính portable.
- Thao tác xóa ảnh tiếp tục sử dụng thư viện `send2trash` để bảo vệ dữ liệu người dùng.
- Cấu trúc mã nguồn mới sẽ thay thế cấu trúc thư mục phẳng hiện tại trong `src/`, các module cũ sẽ được di chuyển và tái cấu trúc vào các tầng Clean Architecture rõ ràng.
