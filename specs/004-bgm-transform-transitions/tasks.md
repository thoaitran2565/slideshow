# Tasks: Nhạc Nền Đa Nguồn (YouTube), Xoay & Lật Ảnh, Đa Hiệu Ứng Chuyển Cảnh

**Input**: Design documents from `specs/004-bgm-transform-transitions/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
**Tests**: Kiểm thử xác thực theo kịch bản trực quan `specs/004-bgm-transform-transitions/quickstart.md`.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Khởi tạo cấu trúc module mới và cập nhật các mô hình miền cơ sở.

- [X] T001 Khởi tạo cấu trúc các package module mới `src/infrastructure/bgm/__init__.py` và `src/presentation/views/transitions/__init__.py`
- [X] T002 [P] Định nghĩa các thực thể miền `BgmConfig`, `ImageTransformState`, `TransitionType`, `TransitionDirection` và mở rộng `ViewerSettings` trong `src/domain/models.py`
- [X] T003 [P] Khai báo cổng trừu tượng `MusicPlayerPort` trong `src/domain/ports.py`
- [X] T004 Cập nhật giá trị mặc định cho các cấu hình BGM và transition trong `JsonSettingsRepository` tại `src/infrastructure/json_settings_repo.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Thiết lập nền tảng hạ tầng phát nhạc Qt và bộ khung hiệu ứng chuyển cảnh trước khi triển khai các User Story.

**⚠️ CRITICAL**: Phải hoàn thành giai đoạn này trước khi triển khai các User Story.

- [X] T005 [P] Xây dựng `BaseBgmProvider` trong `src/infrastructure/bgm/base_provider.py` và triển khai `QtMusicPlayer` (sử dụng `PyQt6.QtMultimedia.QMediaPlayer` và `QAudioOutput`) trong `src/infrastructure/bgm/qt_music_player.py`
- [X] T006 [P] Triển khai trường hợp sử dụng `ManageBgmUseCase` trong `src/application/use_cases.py` để điều phối nguồn phát, âm lượng, chế độ lặp lại và kiểm tra kết nối
- [X] T007 Xây dựng lớp chiến lược trừu tượng `BaseTransitionStrategy` trong `src/presentation/views/transitions/base_transition.py` và bộ điều phối `TransitionEngine` trong `src/presentation/views/transitions/engine.py`

**Checkpoint**: Nền tảng hạ tầng BGM và Transition Engine đã sẵn sàng cho các User Story.

---

## Phase 3: User Story 1 - Phát Nhạc Nền Từ Nguồn Mở Rộng (Nền Tảng YouTube) (Priority: P1) 🎯 MVP

**Goal**: Cho phép người dùng cấu hình URL/Video ID YouTube, nghe thử với thông báo lỗi, phát nhạc nền đồng bộ trình chiếu và điều khiển qua nút BGM trên thanh công cụ.

**Independent Test**: Mở Cài đặt, dán link YouTube, bấm "Nghe thử", xác nhận âm thanh phát và có báo lỗi nếu link hỏng; lưu cấu hình và xác nhận nhạc phát đồng bộ cùng slideshow, nút 🎵 trên thanh điều khiển bật/tắt âm thanh tức thì.

### Implementation for User Story 1

- [X] T008 [US1] Triển khai `YouTubeBgmProvider` trong `src/infrastructure/bgm/youtube_provider.py` sử dụng `yt-dlp` trích xuất luồng audio trực tiếp (`bestaudio/best`, `skip_download=True`) chạy trong luồng nền `QThread` kèm xử lý ngoại lệ mạng
- [X] T009 [US1] Cập nhật `ViewerPresenter` trong `src/presentation/presenter.py` để tích hợp `ManageBgmUseCase`, đồng bộ trạng thái phát/dừng nhạc theo slideshow và xử lý nghe thử/báo lỗi
- [X] T010 [US1] Bổ sung nút BGM (🎵/🔇) trên thanh điều khiển nổi `ControlPanel` trong `src/presentation/views/control_panel.py` với logic bật/tắt nhanh hoặc tự động mở Cài đặt nếu nhạc chưa cấu hình
- [X] T011 [US1] Mở rộng hộp thoại `SettingsDialog` trong `src/presentation/views/settings_dialog.py` với khu vực cấu hình BGM: checkbox bật nhạc, chọn nguồn YouTube, ô nhập URL/Video ID, nút "Nghe thử", nhãn hiển thị trạng thái kết nối/báo lỗi, thanh trượt âm lượng và checkbox lặp lại

**Checkpoint**: User Story 1 hoàn tất - phát nhạc nền YouTube ổn định và điều khiển mượt mà.

---

## Phase 4: User Story 2 - Xoay & Lật Ảnh Linh Hoạt (Priority: P1)

**Goal**: Cho phép xoay 90°/180° và lật ngang/dọc không phá hủy tệp gốc, ghi nhớ góc xoay trong phiên (`Session Transform Cache`) và hỗ trợ phím tắt.

**Independent Test**: Xoay ảnh 90° bằng nút xoay hoặc phím `R`, lật ngang bằng phím `F`; ảnh biến đổi ngay ngắn và căn giữa vừa khung nhìn; chuyển sang ảnh khác rồi quay lại, ảnh cũ vẫn giữ nguyên góc đã xoay; tệp ảnh trên đĩa hoàn toàn không bị thay đổi.

### Implementation for User Story 2

- [X] T012 [US2] Thêm bộ nhớ đệm hiển thị phiên (`transform_cache: dict[str, ImageTransformState]`) và các phương thức `rotate_current`, `flip_current_h`, `flip_current_v`, `reset_current_transform` trong `ViewerPresenter` tại `src/presentation/presenter.py`
- [X] T013 [US2] Triển khai logic biến đổi đồ họa không phá hủy `QTransform` xoay quanh tâm và lật ảnh trên `self.pixmap_item`, đồng bộ căn chỉnh `fit_image_in_view()` trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py`
- [X] T014 [US2] Thêm nút Xoay ảnh nhanh trên thanh điều khiển nổi `ControlPanel` tại `src/presentation/views/control_panel.py` và tích hợp các mục Xoay trái/phải, Lật ngang/dọc trong thực đơn Tùy chọn (`show_options_menu`)
- [X] T015 [US2] Đăng ký hệ thống phím tắt công thái học (`R` xoay phải, `Shift+R` xoay trái, `F` lật ngang, `V` lật dọc, `Ctrl+R` đặt lại) trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py`

**Checkpoint**: User Story 2 hoàn tất - xoay và lật ảnh linh hoạt, bảo vệ dữ liệu gốc tuyệt đối.

---

## Phase 5: User Story 3 - Lựa Chọn & Cấu Hình 5 Hiệu Ứng Chuyển Cảnh (Priority: P2)

**Goal**: Cung cấp 5 hiệu ứng chuyển cảnh phong phú (*Fade, Slide Left, Slide Right, Zoom Fade, None*), tự động đảo chiều khi duyệt lùi (`Prev`) và lưu cấu hình vào `settings.json`.

**Independent Test**: Chọn hiệu ứng "Trượt sang trái (Slide Left)" trong Cài đặt; khi bấm Next ảnh trượt sang trái, khi bấm Prev ảnh tự động đảo chiều trượt sang phải; chọn "Zoom Fade" hoặc "Instant Cut" hoạt động trơn tru.

### Implementation for User Story 3

- [X] T016 [US3] Triển khai 4 lớp chiến lược hiệu ứng cụ thể trong `src/presentation/views/transitions/`: `CrossFadeTransition` (`fade_transition.py`), `SlideTransition` có đảo chiều thông minh (`slide_transition.py`), `ZoomFadeTransition` (`zoom_transition.py`), và `InstantTransition` (`instant_transition.py`)
- [X] T017 [US3] Tích hợp `TransitionEngine` vào quy trình nạp và chuyển ảnh trong `PhotoViewerWindow` tại `src/presentation/views/viewer_window.py` với cơ chế dừng an toàn hoạt ảnh cũ khi chuyển nhanh
- [X] T018 [US3] Bổ sung ComboBox danh sách 5 hiệu ứng chuyển cảnh trong `SettingsDialog` tại `src/presentation/views/settings_dialog.py` và lưu trữ vào `settings.json`

**Checkpoint**: Toàn bộ 3 User Stories đã hoàn tất và kết hợp nhuần nhuyễn.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Đấu nối Dependency Injection tại Composition Root, cập nhật kịch bản đóng gói PyInstaller và xác thực toàn diện.

- [X] T019 Đấu nối khởi tạo `QtMusicPlayer` và `ManageBgmUseCase` vào Composition Root trong `main.py`
- [X] T020 Cập nhật tệp kịch bản đóng gói `slideshow.spec` với `hiddenimports: ['yt_dlp', 'PyQt6.QtMultimedia']` và kiểm thử lệnh đóng gói `python -m PyInstaller -y slideshow.spec`
- [X] T021 Thực hiện kiểm thử xác thực toàn diện 3 kịch bản theo `specs/004-bgm-transform-transitions/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Không phụ thuộc, khởi tạo module và domain models.
- **Foundational (Phase 2)**: Phụ thuộc vào Phase 1; thiết lập `QtMusicPlayer`, `ManageBgmUseCase` và `TransitionEngine`.
- **User Story 1 (Phase 3)**: Phụ thuộc vào Phase 2; hoàn thiện luồng nhạc nền YouTube (MVP).
- **User Story 2 (Phase 4)**: Phụ thuộc vào Phase 2; có thể chạy song song với US1 nếu khác tệp, hoặc tuần tự sau US1.
- **User Story 3 (Phase 5)**: Phụ thuộc vào Phase 2 & T007; hoàn thiện 5 chiến lược hiệu ứng và tích hợp View.
- **Polish (Phase 6)**: Phụ thuộc vào việc hoàn tất cả 3 User Stories.

---

## Parallel Execution Opportunities

- T002 và T003 có thể chạy song song (các file khác nhau trong `src/domain/`).
- T005 và T006 có thể chạy song song (hạ tầng player và use case).
- Sau khi hoàn thành Phase 2, các module của US1 (BGM), US2 (Transform) và US3 (Transitions) có thể được phát triển độc lập theo từng nhánh file chuyên biệt trước khi tích hợp vào `viewer_window.py` và `main.py`.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Hoàn thành Phase 1 (Setup) và Phase 2 (Foundational).
2. Hoàn thành Phase 3: User Story 1 (T008 → T011).
3. Đấu nối `main.py` và kiểm thử tính năng phát nhạc nền YouTube độc lập. Đạt chuẩn MVP!

### Incremental Delivery
1. Bổ sung User Story 2 (T012 → T015) để người dùng có thể xoay và lật ảnh ngay lập tức.
2. Bổ sung User Story 3 (T016 → T018) để nâng tầm thị giác với 5 hiệu ứng chuyển cảnh linh hoạt.
3. Hoàn tất kiểm thử và đóng gói PyInstaller tại Phase 6 (T019 → T021).

