---
description: "Danh sách tác vụ chi tiết triển khai tính năng Khắc phục luồng Bật/Tắt nhạc BGM"
---

# Tasks: Khắc Phục Luồng Bật Nhạc BGM Trên Thanh Option

**Input**: Design documents from `/specs/007-fix-bgm-play-button-flow/`  
**Prerequisites**: [plan.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/plan.md), [spec.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/spec.md), [research.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/research.md), [data-model.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/data-model.md), [contracts/bgm_play_fix_contract.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/contracts/bgm_play_fix_contract.md), [quickstart.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/quickstart.md)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Có thể chạy song song (khác tệp tin, không phụ thuộc nhau)
- **[Story]**: Nhãn phân loại User Story (ví dụ: `[US1]`, `[US2]`)
- Mô tả tác vụ luôn chỉ định đường dẫn tệp cụ thể

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Thiết lập môi trường và cấu hình tệp thử nghiệm tính năng 007

- [X] T001 Khởi tạo tệp kiểm thử tích hợp tự động cho Feature 007 trong `tests/test_feature_007.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Đảm bảo lớp lưu trữ cấu hình tự động đồng bộ cờ kế thừa `bgm_enabled` với tính hợp lệ của `bgm_youtube_url`

- [X] T002 Đồng bộ cờ kế thừa `bgm_enabled` an toàn dựa trên `bool(bgm_youtube_url.strip())` khi nạp và lưu trong `src/infrastructure/json_settings_repo.py`

**Checkpoint**: Lớp lưu trữ cấu hình nhất quán, sẵn sàng cho việc triển khai logic User Story 1 & 2.

---

## Phase 3: User Story 1 - Kích Hoạt Phát Nhạc Ngay Khi Đã Có Cấu Hình Link YouTube (Priority: P1) 🎯 MVP

**Goal**: Khi người dùng nhấn nút "🎵 Bật nhạc" trên thanh công cụ option ngoài màn hình chính và đã có link nhạc trong cấu hình, ứng dụng kích hoạt phát nhạc ngay lập tức, không mở nhầm hộp thoại Cài đặt dù file `settings.json` có cờ `bgm_enabled: false`.

**Independent Test**: Cấu hình `bgm_youtube_url` có link hợp lệ và `bgm_enabled = False`. Nhấn nút BGM; kiểm tra `is_bgm_ready()` trả về `True`, hệ thống gọi phát nhạc và `SettingsDialog` không được mở ra.

### Tests for User Story 1

- [X] T003 [P] [US1] Xây dựng unit/integration test kiểm tra `is_bgm_ready()` và luồng `toggle_bgm_action()` trong `tests/test_feature_007.py`

### Implementation for User Story 1

- [X] T004 [US1] Sửa đổi phương thức `is_bgm_ready()` trong `src/presentation/presenter.py` để chỉ kiểm tra `bool(self.settings.bgm_youtube_url and self.settings.bgm_youtube_url.strip())`
- [X] T005 [US1] Rà soát và xác nhận luồng điều kiện `toggle_bgm_action()` trong `src/presentation/views/viewer_window.py` gọi `presenter.play_bgm()` thay vì mở Cài đặt khi có URL hợp lệ

**Checkpoint**: User Story 1 hoàn thành độc lập và vượt qua kiểm thử; nút BGM ngoài màn hình chính không còn mở Cài đặt khi đã có link.

---

## Phase 4: User Story 2 - Tự Động Nạp Nguồn & Phát Nhạc Khi Khởi Động Ứng Dụng Mới (Priority: P1)

**Goal**: Khi ứng dụng vừa khởi động lần đầu, người dùng bấm nút "🎵 Bật nhạc" ngoài màn hình chính thì nhạc lập tức được nạp (`set_source`), hiển thị trạng thái "⏳ Đang tải..." rồi phát nhạc mà không cần phải vào Cài đặt bấm "Nghe thử" để mồi nguồn trước.

**Independent Test**: Khởi tạo `ManageBgmUseCase` với `QtMusicPlayer` chưa có nguồn phát (`current_target = ""`); gọi `play()`; xác nhận `music_player.set_source(url)` được tự động kích hoạt và player chuyển sang trạng thái nạp.

### Tests for User Story 2

- [X] T006 [P] [US2] Xây dựng test case kiểm tra `ManageBgmUseCase.play()` tự động nạp nguồn khi player chưa có target trong `tests/test_feature_007.py`

### Implementation for User Story 2

- [X] T007 [US2] Nâng cấp phương thức `play()` trong `src/application/use_cases.py` để tự động kiểm tra `player_target` và gọi `self.music_player.set_source(url)` khi `current_target != url`

**Checkpoint**: User Story 2 hoàn thành độc lập; khi mở app lên bấm phát nhạc, hệ thống tự động nạp nguồn và phát âm thanh ngay tức thì.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Đảm bảo toàn bộ hệ thống hoạt động ổn định, vượt qua mọi bài kiểm thử và đóng gói thành công.

- [X] T008 [P] Chạy toàn bộ test suite xác thực tự động trong `tests/test_feature_007.py` và kiểm tra hồi quy với `tests/test_feature_006.py`
- [X] T009 Xác thực kiểm thử theo các kịch bản trong `specs/007-fix-bgm-play-button-flow/quickstart.md`
- [X] T010 [P] Đóng gói ứng dụng thành file thực thi độc lập bằng lệnh `python -m PyInstaller -y slideshow.spec` và xác nhận file `dist/Slideshow.exe` hoạt động không lỗi

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Có thể bắt đầu ngay lập tức.
- **Foundational (Phase 2)**: Phụ thuộc vào Phase 1; chuẩn bị lớp lưu trữ cấu hình nhất quán.
- **User Story 1 (Phase 3)**: Phụ thuộc vào Phase 2. Giải quyết lỗi mở Cài đặt nhầm.
- **User Story 2 (Phase 4)**: Phụ thuộc vào Phase 2 (có thể triển khai song song hoặc nối tiếp sau US1). Giải quyết lỗi không phản hồi khi mới mở app.
- **Polish (Phase 5)**: Phụ thuộc vào việc hoàn tất cả User Story 1 và User Story 2.

### User Story Dependencies

- **User Story 1 (P1)**: Chỉnh sửa tại `src/presentation/presenter.py` và `src/presentation/views/viewer_window.py`.
- **User Story 2 (P1)**: Chỉnh sửa tại `src/application/use_cases.py`.
- Hai story độc lập về mặt tầng kiến trúc (Presentation vs Application), hỗ trợ kiểm thử riêng biệt.

---

## Parallel Opportunities

- **T003** và **T006** có thể được phát triển song song trong tệp test `tests/test_feature_007.py`.
- **T004** (`presenter.py`) và **T007** (`use_cases.py`) thuộc hai tầng kiến trúc khác nhau và có thể chỉnh sửa độc lập.
- **T008** và **T010** có thể kiểm tra song song sau khi hoàn tất mã nguồn.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. **Bước 1**: Hoàn tất T001, T002 chuẩn bị môi trường và cấu hình.
2. **Bước 2**: Triển khai T003, T004, T005 giải quyết dứt điểm lỗi mở nhầm Cài đặt (User Story 1).
3. **Bước 3**: Triển khai T006, T007 kích hoạt cơ chế tự nạp nguồn khi mở app (User Story 2).
4. **Bước 4**: Chạy kiểm thử tự động T008, kiểm thử nhanh T009 và đóng gói bản build PyInstaller T010.

