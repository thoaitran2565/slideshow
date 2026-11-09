# Tasks: Nâng Cấp Điều Khiển Nhạc Nền (Live Volume, Quick Popup, BGM Label & Source Protection)

**Input**: Design documents from `specs/005-bgm-controls-enhancement/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
**Tests**: Kiểm thử xác thực theo kịch bản trực quan `specs/005-bgm-controls-enhancement/quickstart.md`.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions.

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Mở rộng các phương thức điều phối âm lượng thời gian thực trong Presenter trước khi tích hợp vào các thành phần giao diện.

- [X] T001 Mở rộng phương thức `set_bgm_volume(self, volume: int, persist: bool = False)` và `persist_bgm_volume(self, volume: int)` trong `ViewerPresenter` tại `src/presentation/presenter.py` để hỗ trợ cập nhật âm thanh loa tức thời và tùy chọn lưu đĩa

---

## Phase 2: User Story 1 - Cập Nhật Âm Lượng Nhạc Nền Thời Gian Thực (Priority: P1) 🎯 MVP

**Goal**: Cho phép người dùng di chuyển thanh trượt âm lượng và nhận phản hồi âm thanh loa thay đổi ngay lập tức khi đang bấm "Nghe thử" trong Cài đặt hoặc khi đang trình chiếu slideshow.

**Independent Test**: Mở Cài đặt, bấm "Nghe thử" bài nhạc YouTube; kéo thanh trượt từ 100% xuống 20%; xác nhận âm lượng loa giảm ngay tức thì mà không cần dừng và nghe thử lại.

### Implementation for User Story 1

- [X] T002 [US1] Kết nối sự kiện `valueChanged` của `self.slider_bgm_volume` trực tiếp tới `presenter.set_bgm_volume(val, persist=False)` trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py`
- [X] T003 [US1] Bổ sung sự kiện `sliderReleased` trên `self.slider_bgm_volume` để kích hoạt ghi nhận cấu hình âm lượng mới trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py`

**Checkpoint**: User Story 1 hoàn tất - điều chỉnh âm lượng phản hồi thời gian thực mượt mà.

---

## Phase 3: User Story 2 - Popup Chỉnh Âm Lượng Nhanh Bằng Chuột Phải (Priority: P1)

**Goal**: Cung cấp widget popup chỉnh âm lượng nhanh xuất hiện ngay trên nút BGM khi nhấp chuột phải trên thanh điều khiển nổi, hỗ trợ kéo thanh trượt chỉnh âm thanh trực tiếp.

**Independent Test**: Nhấp chuột phải vào nút BGM trên thanh Control Panel; một popup thanh trượt âm lượng nhỏ gọn xuất hiện ngay phía trên nút; kéo thanh trượt để chỉnh âm lượng bài nhạc đang phát; nhấp ra ngoài để đóng popup.

### Implementation for User Story 2

- [X] T004 [US2] Xây dựng lớp giao diện `QuickVolumePopup(QWidget)` trong `src/presentation/views/control_panel.py` với cờ `Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint`, Dark Theme viền `#00adb5`, gồm icon loa, slider ngang, nhãn phần trăm và tín hiệu `volume_changed`, `volume_released`
- [X] T005 [US2] Cấu hình chính sách `CustomContextMenu` trên `self.btn_bgm` trong `ControlPanel` tại `src/presentation/views/control_panel.py` và triển khai phương thức `_show_volume_popup` tính toán tọa độ neo toàn cục ngay phía trên nút
- [X] T006 [US2] Đấu nối tín hiệu `bgm_volume_changed` và `bgm_volume_saved` từ `ControlPanel` tới các hàm điều phối `presenter.set_bgm_volume` và `presenter.persist_bgm_volume` trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py`

**Checkpoint**: User Story 2 hoàn tất - popup chỉnh âm lượng nhanh hoạt động độc lập và trực quan.

---

## Phase 4: User Story 3 - Chuẩn Hóa Nhãn Nút BGM & Khóa Nguồn Chưa Khả Dụng (Priority: P2)

**Goal**: Hiển thị rõ tiêu đề "Bật nhạc" / "Tắt nhạc" trên nút BGM của thanh điều khiển nổi, nới rộng bố cục thanh điều khiển và vô hiệu hóa các tùy chọn nguồn nhạc chưa phát triển trong Cài đặt.

**Independent Test**: Quan sát nút BGM thấy rõ chữ "🎵 Bật nhạc" (khi tắt) và "🔇 Tắt nhạc" (khi bật); mở Cài đặt thấy các mục Spotify/Local file bị làm mờ và không thể click chọn.

### Implementation for User Story 3

- [X] T007 [US3] Cập nhật hàm `set_bgm_state` trong `ControlPanel` tại `src/presentation/views/control_panel.py` để cập nhật tiêu đề nút thành `"🎵 Bật nhạc"` hoặc `"🔇 Tắt nhạc"` kèm tooltip tương ứng
- [X] T008 [US3] Điều chỉnh độ rộng thanh điều khiển nổi `panel_width = 760` và căn chỉnh layout/min-width nút trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py` để hiển thị chữ trọn vẹn
- [X] T009 [US3] Áp dụng `QStandardItemModel` trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py` để vô hiệu hóa (`item.setEnabled(False)`) các mục nguồn nhạc chưa hỗ trợ (`"local"`, `"spotify"`), chỉ cho phép chọn `"youtube"`

**Checkpoint**: Toàn bộ 3 User Stories hoàn thành và tích hợp liền mạch.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Xác thực toàn diện các kịch bản kiểm thử và kiểm tra đóng gói ứng dụng.

- [X] T010 Thực hiện kiểm thử xác thực toàn diện 4 kịch bản theo `specs/005-bgm-controls-enhancement/quickstart.md`
- [X] T011 Kiểm tra khả năng đóng gói PyInstaller độc lập với lệnh `python -m PyInstaller -y slideshow.spec` xác nhận tính toàn vẹn của tệp thực thi Windows

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: Không phụ thuộc - có thể bắt đầu ngay.
- **User Story 1 (Phase 2)**: Phụ thuộc vào Phase 1 (`ViewerPresenter.set_bgm_volume`).
- **User Story 2 (Phase 3)**: Phụ thuộc vào Phase 1; có thể chạy độc lập hoặc tiếp nối sau US1.
- **User Story 3 (Phase 4)**: Có thể triển khai độc lập hoặc song song với US1 và US2.
- **Polish (Phase 5)**: Phụ thuộc vào việc hoàn tất cả 3 User Stories.

---

## Parallel Execution Opportunities

- T002 và T003 có thể thực hiện liên hoàn trong `settings_dialog.py`.
- T004 và T005 có thể thực hiện chung trong `control_panel.py`.
- T007 và T008 có thể làm song song với việc hoàn thiện dialog ở T009.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Hoàn thành Phase 1 (Foundational: T001).
2. Hoàn thành Phase 2 (User Story 1: T002, T003).
3. Kiểm thử ngay tính năng Live Volume trong Cài đặt. Đạt chuẩn MVP!

### Incremental Delivery
1. Bổ sung User Story 2 (T004 → T006) để mang lại lối tắt chỉnh âm lượng chuột phải cực kỳ tiện lợi trên màn hình chính.
2. Bổ sung User Story 3 (T007 → T009) để hoàn thiện nhãn nút BGM và ngăn chặn lỗi chọn nguồn chưa khả dụng.
3. Chạy xác thực và kiểm tra đóng gói tại Phase 5 (T010, T011).

