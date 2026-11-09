# Tasks: Giới Hạn Mức Thu Nhỏ Tối Thiểu (Chỉ Cho Phép Phóng To Chi Tiết)

**Input**: Design documents from `specs/003-restrict-min-zoom/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/view_interaction_contract.md`, `quickstart.md`
**Tests**: Kiểm thử xác thực theo kịch bản trực quan `specs/003-restrict-min-zoom/quickstart.md`.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- All tasks include exact file paths.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Khởi tạo cấu trúc dữ liệu và các hằng số điều khiển tỷ lệ phóng đại (Zoom State) trong Presentation View.

- [X] T001 Khởi tạo các thuộc tính điều khiển tỷ lệ zoom `self.current_zoom = 1.0`, `self.min_zoom = 1.0`, `self.max_zoom = 20.0`, `self.zoom_step = 1.15` trong phương thức `__init__` của `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Thiết lập hàm chuẩn hóa mốc kích thước hiển thị gốc và đồng bộ tỷ lệ zoom cơ sở ($1.0x$) trước khi xử lý tương tác chuột.

**⚠️ CRITICAL**: Phải hoàn thành giai đoạn này trước khi triển khai các User Story.

- [X] T002 Cập nhật phương thức `fit_image_in_view()` trong `src/presentation/views/viewer_window.py` để đồng bộ `self.current_zoom = 1.0` khi gọi `self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)`

**Checkpoint**: Nền tảng điều khiển tỷ lệ zoom đã sẵn sàng cho các User Story.

---

## Phase 3: User Story 1 - Ngăn Chặn Thu Nhỏ Dưới Kích Thước Vừa Khung Nhìn (Priority: P1) 🎯 MVP

**Goal**: Ngăn chặn hoàn toàn thao tác cuộn chuột làm ảnh bị co nhỏ hơn kích thước vừa vặn ban đầu (Fit in View).

**Independent Test**: Mở ứng dụng, cuộn chuột xuống liên tục khi ảnh ở mức ban đầu; ảnh không thay đổi kích thước và giữ nguyên trạng thái Fit in View.

### Implementation for User Story 1

- [X] T003 [US1] Cập nhật phương thức `wheelEvent()` trong `src/presentation/views/viewer_window.py` để bỏ qua sự kiện cuộn xuống (`event.angleDelta().y() < 0`) khi `self.current_zoom <= 1.001` (No-op, không cho phép thu nhỏ dưới $1.0x$)
- [X] T004 [US1] Điều chỉnh chế độ kéo rê chuột `ScrollHandDrag` trong `src/presentation/views/viewer_window.py` để chỉ cho phép Pan khi `self.current_zoom > 1.0`, ngăn ảnh bị trôi lệch khi đang ở mức $1.0x$

**Checkpoint**: User Story 1 hoàn tất - ảnh không thể bị thu nhỏ dưới kích thước vừa khung hình ban đầu.

---

## Phase 4: User Story 2 - Phóng To Chi Tiết & Thu Nhỏ Mượt Mà Về Kích Thước Gốc (Priority: P1)

**Goal**: Cho phép phóng to mượt mà lên tới $20.0x$ và khi thu nhỏ xuống thì kẹp (clamp) chính xác về mức $1.0x$ kèm căn giữa.

**Independent Test**: Cuộn chuột lên 3 lần để phóng to chi tiết ảnh, sau đó cuộn chuột xuống 5 lần; ảnh thu nhỏ mượt mà và dừng lại chính xác tại mức $1.0x$ vừa khít khung nhìn.

### Implementation for User Story 2

- [X] T005 [US2] Triển khai logic phóng to khi cuộn chuột lên (`event.angleDelta().y() > 0`) trong `wheelEvent()` tại `src/presentation/views/viewer_window.py` với bước phóng đại `self.zoom_step = 1.15`, kiểm soát trần tối đa `self.max_zoom = 20.0`
- [X] T006 [US2] Triển khai thuật toán kẹp giá trị khi cuộn chuột xuống (`event.angleDelta().y() < 0`) trong `wheelEvent()` tại `src/presentation/views/viewer_window.py`: nếu `new_zoom <= 1.0` thì kẹp về `1.0` và gọi `self.fit_image_in_view()`, ngược lại chia tỷ lệ cho `self.zoom_step`

**Checkpoint**: User Story 2 hoàn tất - người dùng có thể phóng to soi chi tiết và thu nhỏ an toàn về điểm xuất phát.

---

## Phase 5: User Story 3 - Tự Động Đặt Lại Tỷ Lệ Chuẩn Khi Đổi Ảnh Hoặc Đổi Cửa Sổ (Priority: P2)

**Goal**: Tự động reset tỷ lệ zoom về $1.0x$ và căn chỉnh lại khung nhìn khi chuyển sang ảnh mới hoặc resize cửa sổ.

**Independent Test**: Đang phóng to ảnh bất kỳ, bấm phím mũi tên Phải hoặc đổi kích thước cửa sổ (F11); ảnh lập tức trở về trạng thái vừa khít khung nhìn ở mốc $1.0x$.

### Implementation for User Story 3

- [X] T007 [US3] Xác nhận và bảo đảm việc gọi `fit_image_in_view()` trong `show_image()` tại `src/presentation/views/viewer_window.py` luôn reset `self.current_zoom = 1.0` khi chuyển ảnh (thủ công hoặc tự động)
- [X] T008 [US3] Xác nhận và bảo đảm `resizeEvent()` tại `src/presentation/views/viewer_window.py` gọi `fit_image_in_view()` để đồng bộ lại tỷ lệ zoom và mốc kích thước vừa vặn theo kích thước cửa sổ mới

**Checkpoint**: Toàn bộ 3 User Stories đã hoàn chỉnh và hoạt động nhất quán.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Kiểm thử xác thực theo kịch bản và đảm bảo tính sẵn sàng biên dịch PyInstaller.

- [X] T009 Thực hiện kiểm thử xác thực theo 3 kịch bản trong `specs/003-restrict-min-zoom/quickstart.md`
- [X] T010 [P] Đóng gói thử nghiệm gói thực thi Windows `python -m PyInstaller -y slideshow.spec` để xác nhận không phát sinh lỗi biên dịch

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Không phụ thuộc, thực hiện đầu tiên.
- **Foundational (Phase 2)**: Phụ thuộc vào Phase 1, tạo nền tảng cho tất cả User Stories.
- **User Story 1 (Phase 3)**: Phụ thuộc vào Phase 2. Đạt chuẩn MVP.
- **User Story 2 (Phase 4)**: Phụ thuộc vào Phase 3 (kế thừa logic kiểm soát zoom).
- **User Story 3 (Phase 5)**: Phụ thuộc vào Phase 4 (đảm bảo reset zoom đúng trên toàn bộ vòng đời hiển thị).
- **Polish (Phase 6)**: Phụ thuộc vào việc hoàn thành tất cả User Stories.

### User Story Dependencies

- **US1 (P1)**: Core MVP - Chặn thu nhỏ dưới kích thước gốc.
- **US2 (P1)**: Mở rộng US1 - Cho phép phóng to tối đa $20.0x$ và thu nhỏ kẹp về $1.0x$.
- **US3 (P2)**: Hoàn thiện trải nghiệm - Tự động reset về $1.0x$ khi chuyển ảnh và resize.

---

## Parallel Execution Examples

Tất cả các tác vụ mã nguồn đều tập trung tại tệp Presentation View `src/presentation/views/viewer_window.py`, do đó chuỗi thực thi code diễn ra tuần tự từ T001 đến T008 để đảm bảo tính toàn vẹn trạng thái. T010 có thể chạy độc lập trong giai đoạn Polish.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Hoàn thành Phase 1 (T001) và Phase 2 (T002).
2. Hoàn thành Phase 3: User Story 1 (T003, T004).
3. **VALIDATE**: Thử cuộn chuột xuống xem ảnh có bị thu nhỏ dưới kích thước gốc không. Đạt chuẩn MVP!

### Incremental Delivery
1. Bổ sung User Story 2 (T005, T006) để hoàn thiện tính năng phóng to chi tiết và thu nhỏ an toàn.
2. Bổ sung User Story 3 (T007, T008) để đồng bộ trạng thái khi chuyển ảnh hoặc resize.
3. Chạy toàn bộ kịch bản kiểm thử tại Phase 6 (T009, T010).

