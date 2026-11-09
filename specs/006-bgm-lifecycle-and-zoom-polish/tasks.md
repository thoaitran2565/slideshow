# Tasks: Tinh Chỉnh Vòng Đời Nhạc Nền, Lớp Phủ Chống Click Xuyên & Tối Ưu Mượt Mà Hiệu Ứng Zoom Fade

**Input**: Design documents from `specs/006-bgm-lifecycle-and-zoom-polish/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
**Tests**: Kiểm thử xác thực theo kịch bản trực quan `specs/006-bgm-lifecycle-and-zoom-polish/quickstart.md`.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions.

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Mở rộng mô hình miền và hạ tầng player với trạng thái phát và bộ đếm Safety Timeout 15s.

- [X] T001 [P] Định nghĩa `BgmPlaybackState` (`STOPPED`, `LOADING`, `PLAYING`, `ERROR`) trong `src/domain/models.py`
- [X] T002 [P] Cập nhật `QtMusicPlayer` trong `src/infrastructure/bgm/qt_music_player.py` với `QTimer` 15s Safety Timeout, cơ chế `cancel_loading()` và callback trạng thái phát nhạc

---

## Phase 2: User Story 1 - Tách Biệt Độc Lập Vòng Đời Nhạc Nền & Hợp Nhất Trải Nghiệm Cài Đặt (Priority: P1) 🎯 MVP

**Goal**: Đảm bảo nhạc nền hoạt động độc lập không bị ảnh hưởng bởi Pause/Play của slide, loại bỏ ô checkbox kích hoạt trong Cài đặt và tự động ngắt BGM khi sửa link hoặc bấm nghe thử.

**Independent Test**: Bật nhạc nền đang phát; bấm Phím cách (Space) để Pause slideshow; xác nhận slide dừng nhưng âm thanh vẫn tiếp tục phát; mở Cài đặt gõ link mới hoặc bấm "Nghe thử"; xác nhận nhạc nền slideshow bên ngoài tự động tắt.

### Implementation for User Story 1

- [X] T003 [US1] Tách rời lệnh Pause/Play slideshow khỏi BGM trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py` (slide dừng nhưng nhạc vẫn phát bình thường)
- [X] T004 [US1] Loại bỏ checkbox `chk_bgm_enable` ("Kích hoạt nhạc nền khi trình chiếu") khỏi giao diện và logic lưu dữ liệu trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py`
- [X] T005 [US1] Bổ sung cơ chế tự động ngắt nhạc nền slideshow khi người dùng sửa link YouTube (`textEdited`) hoặc bấm nút "▶ Nghe Thử" trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py`

**Checkpoint**: User Story 1 hoàn tất - vòng đời BGM hoàn toàn độc lập và ngăn chặn triệt để xung đột âm thanh.

---

## Phase 3: User Story 2 - Trạng Thái Đang Tải Nhạc (Loading) & Giới Hạn Thời Gian Chờ An Toàn (Priority: P1)

**Goal**: Hiển thị trạng thái `"⏳ Đang tải..."` và khóa nút BGM chống spam click; tab Cài đặt hiển thị loading; timeout 15s tự động hủy luồng và thông báo lỗi nếu quá hạn hoặc link hỏng.

**Independent Test**: Bấm "Bật nhạc"; nút BGM đổi sang `"⏳ Đang tải..."` và bị vô hiệu hóa; sau khi phát thành công đổi sang `"🔇 Tắt nhạc"`; nếu mạng treo, đúng 15 giây sau nút phục hồi về `"🎵 Bật nhạc"` kèm tooltip báo lỗi.

### Implementation for User Story 2

- [X] T006 [US2] Thêm hàm `set_bgm_loading(self, is_loading: bool, error_msg: Optional[str] = None)` trên `ControlPanel` tại `src/presentation/views/control_panel.py` để hiển thị nhãn `"⏳ Đang tải..."` và khóa click chống spam
- [X] T007 [US2] Cập nhật giao diện tab Nhạc Nền trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py` để hiển thị trạng thái loading và khóa controls khi đang nạp nhạc
- [X] T008 [US2] Đấu nối tín hiệu trạng thái `BgmPlaybackState` và xử lý timeout 15s từ `QtMusicPlayer` qua `ViewerPresenter` tới `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py`

**Checkpoint**: User Story 2 hoàn tất - trải nghiệm nạp nhạc bất đồng bộ rõ ràng và an toàn tuyệt đối.

---

## Phase 4: User Story 3 - Lớp Phủ Chống Click Xuyên Khi Đóng Popup Âm Lượng (Priority: P2)

**Goal**: Kích hoạt lớp phủ trong suốt chặn sự kiện khi Quick Volume Popup đang mở, đảm bảo cú nhấp chuột ra ngoài chỉ đóng thanh âm lượng mà không vô tình kích hoạt các nút bên dưới.

**Independent Test**: Nhấp chuột phải vào nút BGM để mở thanh âm lượng nổi; rê chuột nhấp vào nút "Pause" hoặc vào vùng ảnh; popup âm lượng biến mất nhưng slideshow KHÔNG bị đổi trạng thái và ảnh KHÔNG bị phóng to/chuyển đổi.

### Implementation for User Story 3

- [X] T009 [US3] Xây dựng lớp `BackdropOverlay(QWidget)` trong suốt trong `src/presentation/views/control_panel.py` bắt sự kiện `mousePressEvent` để đóng popup âm lượng và tiêu thụ sự kiện
- [X] T010 [US3] Tích hợp `BackdropOverlay` vào quy trình mở và đóng `QuickVolumePopup` trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py`

**Checkpoint**: User Story 3 hoàn tất - loại bỏ hoàn toàn hiện tượng click nhầm khi đóng popup âm lượng.

---

## Phase 5: User Story 4 - Chuẩn Hóa Khung Hình Mượt Mà Cho Hiệu Ứng Zoom Fade (Priority: P2)

**Goal**: Khắc phục triệt để hiện tượng giật nảy khung hình của hiệu ứng Zoom Fade khi chuyển đổi giữa các bức ảnh có kích thước và độ phân giải chênh lệch lớn.

**Independent Test**: Chọn hiệu ứng "Zoom Fade" trong Cài đặt; duyệt chuyển tiếp liên tục giữa các ảnh có kích thước rất khác nhau; hai bức ảnh hòa quyện êm ái, tỷ lệ co giãn đồng nhất từ đầu đến cuối hiệu ứng ở 60 FPS.

### Implementation for User Story 4

- [X] T011 [US4] Nâng cấp thuật toán `ZoomFadeTransition` trong `src/presentation/views/transitions/zoom_transition.py` để tiền tính toán tỉ lệ fit vừa vặn viewport trước khi bắt đầu hòa trộn, đảm bảo chuyển động đồng tâm 60 FPS không giật nảy

**Checkpoint**: Toàn bộ 4 User Stories đã hoàn thành và tích hợp liền mạch.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Xác thực toàn diện các kịch bản kiểm thử và kiểm tra đóng gói ứng dụng.

- [X] T012 Thực hiện kiểm thử xác thực toàn diện 4 kịch bản theo `specs/006-bgm-lifecycle-and-zoom-polish/quickstart.md`
- [X] T013 Kiểm tra khả năng đóng gói PyInstaller độc lập với lệnh `python -m PyInstaller -y slideshow.spec` xác nhận tính toàn vẹn của tệp thực thi Windows

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: Không phụ thuộc - có thể bắt đầu ngay.
- **User Story 1 (Phase 2)**: Phụ thuộc vào Phase 1; có thể chạy độc lập.
- **User Story 2 (Phase 3)**: Phụ thuộc vào Phase 1 & T002 (QtMusicPlayer timeout).
- **User Story 3 (Phase 4)**: Có thể triển khai song song hoặc sau US1/US2.
- **User Story 4 (Phase 5)**: Độc lập với các story BGM, tập trung vào `zoom_transition.py`.
- **Polish (Phase 6)**: Phụ thuộc vào việc hoàn tất cả 4 User Stories.

---

## Parallel Execution Opportunities

- T001 và T002 có thể triển khai song song.
- T011 (Zoom Fade) có thể triển khai độc lập song song với các công việc BGM (T003 - T010).
- T009 và T010 có thể triển khai song song với T004 và T005.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Hoàn thành Phase 1 (Foundational: T001, T002).
2. Hoàn thành Phase 2 (User Story 1: T003 → T005).
3. Kiểm thử ngay tính năng tách biệt BGM khỏi slideshow và bỏ checkbox Cài đặt. Đạt chuẩn MVP!

### Incremental Delivery
1. Bổ sung User Story 2 (T006 → T008) để có trạng thái Loading `"⏳ Đang tải..."` và timeout an toàn 15s.
2. Bổ sung User Story 3 (T009, T010) để có lớp phủ chống click xuyên khi mở popup âm lượng.
3. Bổ sung User Story 4 (T011) để hoàn thiện độ mượt mà tuyệt đối của Zoom Fade.
4. Chạy xác thực và kiểm tra đóng gói tại Phase 6 (T012, T013).

