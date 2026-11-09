---
description: "Danh sách tác vụ triển khai tính năng tinh chỉnh vòng đời BGM & khởi tạo âm lượng"
---

# Tasks: Tinh Chỉnh Vòng Đời BGM Trong Cài Đặt & Khởi Tạo Âm Lượng

**Input**: Design documents from `/specs/008-fix-bgm-settings-and-volume/`  
**Prerequisites**: [plan.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/plan.md), [spec.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/spec.md), [research.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/research.md), [data-model.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/data-model.md), [contracts/bgm_lifecycle_volume_contract.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/contracts/bgm_lifecycle_volume_contract.md), [quickstart.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/quickstart.md)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Có thể chạy song song (khác tệp tin, không phụ thuộc nhau)
- **[Story]**: Phân loại User Story (`[US1]`, `[US2]`, `[US3]`)
- Mô tả tác vụ luôn chỉ định đường dẫn tệp cụ thể

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Thiết lập môi trường và cấu hình tệp thử nghiệm tính năng 008

- [X] T001 Khởi tạo tệp kiểm thử tự động cho Feature 008 trong `tests/test_feature_008.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Bổ sung phương thức cập nhật cấu hình BGM không nạp lại nguồn phát ở tầng Application và Presenter

- [X] T002 Bổ sung phương thức `apply_settings_without_reload(config: BgmConfig)` trong `src/application/use_cases.py` và `presenter.py` để cập nhật volume/loop mà không nạp lại nguồn

**Checkpoint**: Tầng Application & Presenter sẵn sàng hỗ trợ cập nhật âm lượng/lặp mà không ngắt luồng audio.

---

## Phase 3: User Story 1 - Duy Trì Nhạc Nền Khi Đóng/Hủy Hộp Thoại Cài Đặt (Priority: P1) 🎯 MVP

**Goal**: Đóng hộp thoại Cài đặt (Hủy, Esc, nút X) không làm tắt nhạc nền đang phát ngoài màn hình chính, chỉ dừng âm thanh khi người dùng đang bấm "Nghe thử".

**Independent Test**: Kích hoạt phát nhạc nền; mở Cài đặt (không bấm nghe thử); nhấn "Hủy" hoặc phím Esc; xác nhận nhạc nền vẫn tiếp tục phát.

### Tests for User Story 1

- [X] T003 [P] [US1] Xây dựng test case kiểm tra việc đóng Cài đặt không gọi `stop()` khi `is_testing_audio == False` trong `tests/test_feature_008.py`

### Implementation for User Story 1

- [X] T004 [US1] Cập nhật phương thức `stop_test_audio()` trong `src/presentation/views/settings_dialog.py` chỉ gọi dừng phát khi `self.is_testing_audio == True`

**Checkpoint**: Đóng hoặc Hủy Cài đặt không còn làm ngắt nhạc nền ngoài màn hình chính.

---

## Phase 4: User Story 2 - Giữ Nhạc Phát Liên Tục Khi Lưu Cài Đặt Không Thay Đổi Nguồn Nhạc (Priority: P1)

**Goal**: Khi bấm "Lưu" trong Cài đặt mà URL và nguồn nhạc không đổi (ví dụ chỉ đổi màu nền hoặc thời gian slideshow), nhạc nền đang phát tiếp tục phát liền mạch. Chỉ dừng bài cũ và nạp bài mới khi URL hoặc nguồn phát thực sự thay đổi.

**Independent Test**: Phát nhạc nền; mở Cài đặt, đổi thời gian ảnh từ 3s lên 5s (giữ nguyên link nhạc); nhấn "Lưu"; xác nhận bài hát đang phát không bị ngắt quãng.

### Tests for User Story 2

- [X] T005 [P] [US2] Xây dựng test case kiểm tra `save_data()` không gọi `set_source()` hoặc `stop_bgm()` khi link không thay đổi trong `tests/test_feature_008.py`

### Implementation for User Story 2

- [X] T006 [US2] Lưu vết nguồn ban đầu `initial_youtube_url` và `initial_bgm_source` khi mở hộp thoại trong `src/presentation/views/settings_dialog.py`
- [X] T007 [US2] Cập nhật phương thức `save_data()` trong `src/presentation/views/settings_dialog.py` so sánh URL và chỉ dừng/nạp lại khi có thay đổi thực tế

**Checkpoint**: Lưu Cài đặt các thông số khác không làm gián đoạn bài hát đang nghe.

---

## Phase 5: User Story 3 - Áp Dụng Chính Xác Mức Âm Lượng Đã Lưu Ngay Khi Khởi Động Ứng Dụng (Priority: P1)

**Goal**: Khởi động ứng dụng trong phiên mới và bấm Bật nhạc, âm lượng phát ra đúng chính xác với mức âm lượng người dùng đã lưu trước đó (không dùng mặc định 70%).

**Independent Test**: Cấu hình âm lượng 25% trong `settings.json`; khởi động ứng dụng; bấm Bật nhạc; xác nhận âm lượng trình phát và thanh trượt option đều là 25%.

### Tests for User Story 3

- [X] T008 [P] [US3] Xây dựng test case kiểm tra việc đồng bộ âm lượng từ cấu hình khi khởi động và khi gọi `play()` trong `tests/test_feature_008.py`

### Implementation for User Story 3

- [X] T009 [US3] Khởi tạo âm lượng `music_player.set_volume(settings.bgm_volume)` ngay sau khi load settings trong `main.py`
- [X] T010 [US3] Bổ sung lệnh đồng bộ `self.music_player.set_volume(config.volume)` trong `ManageBgmUseCase.play()` trong `src/application/use_cases.py`

**Checkpoint**: Âm lượng nhạc nền luôn chuẩn xác ngay từ khoảnh khắc phát đầu tiên sau khi khởi động app.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Đảm bảo chất lượng toàn diện, vượt qua mọi bài kiểm thử tự động và đóng gói thành công.

- [X] T011 [P] Chạy toàn bộ test suite xác thực tự động trong `tests/test_feature_008.py` và kiểm tra hồi quy với `tests/test_feature_007.py`
- [X] T012 Xác thực theo các kịch bản kiểm thử trong `specs/008-fix-bgm-settings-and-volume/quickstart.md`
- [X] T013 [P] Đóng gói ứng dụng thành file thực thi độc lập bằng lệnh `python -m PyInstaller -y slideshow.spec` và xác nhận file `dist/Slideshow.exe` hoạt động tốt

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Bắt đầu ngay lập tức.
- **Foundational (Phase 2)**: Chuẩn bị phương thức `apply_settings_without_reload` trước khi tích hợp vào US2.
- **User Story 1 (Phase 3)**: Xử lý `stop_test_audio()` trong `settings_dialog.py`.
- **User Story 2 (Phase 4)**: Xử lý `save_data()` trong `settings_dialog.py` (sử dụng method từ Phase 2).
- **User Story 3 (Phase 5)**: Xử lý âm lượng trong `main.py` và `use_cases.py`.
- **Polish (Phase 6)**: Nghiệm thu toàn diện sau khi hoàn thành cả 3 stories.

---

## Parallel Opportunities

- **T003**, **T005**, **T008** có thể được triển khai song song trong tệp test `tests/test_feature_008.py`.
- **T009** (`main.py`) và **T010** (`use_cases.py`) có thể chạy song song với các sửa đổi trên view `settings_dialog.py`.
- **T011** và **T013** chạy song song ở giai đoạn nghiệm thu.

