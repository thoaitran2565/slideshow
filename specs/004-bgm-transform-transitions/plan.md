# Implementation Plan: Nhạc Nền Đa Nguồn (YouTube), Xoay & Lật Ảnh, Đa Hiệu Ứng Chuyển Cảnh

**Branch**: `004-bgm-transform-transitions` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/004-bgm-transform-transitions/spec.md`

## Summary

Triển khai gói 3 cải tiến đa phương tiện và công thái học hiển thị cốt lõi:
1. **Dịch vụ nhạc nền đa nguồn**: Thiết kế cổng trừu tượng `MusicPlayerPort` dạng mở rộng, hiện thực hóa bộ phát YouTube đầu tiên qua `yt-dlp` stream extraction (non-blocking) kết hợp `PyQt6.QtMultimedia.QMediaPlayer`. Bổ sung nút BGM trên thanh Control Panel, nút "Nghe thử" và báo lỗi trực quan trong hộp thoại Cài đặt.
2. **Xoay & Lật ảnh không phá hủy**: Hỗ trợ xoay 90°/180° và lật ngang/dọc qua `QTransform` trên canvas hiển thị, tích hợp bộ nhớ đệm trạng thái phiên (`Session Transform Cache`), phím tắt công thái học (`R`, `Shift+R`, `F`, `V`), bảo vệ 100% dữ liệu tệp gốc trên đĩa.
3. **Bộ điều phối chuyển cảnh đa hiệu ứng**: Xây dựng kiến trúc `TransitionEngine` mở rộng dạng Pluggable Strategy với 5 hiệu ứng ban đầu (*Fade, Slide Left, Slide Right, Zoom Fade, None*), tự động đảo chiều khi duyệt lùi ảnh (`Prev`), lưu trữ bền vững vào `settings.json`.

## Technical Context

**Language/Version**: Python 3.10+ (PyQt6 6.4+).

**Primary Dependencies**: `PyQt6` (`QtWidgets`, `QtGui`, `QtCore`, `QtMultimedia`), `yt-dlp` (`2026.10+`).

**Storage**: Tệp cấu hình JSON duy nhất `settings.json` thông qua `JsonSettingsRepository`.

**Testing**: Kiểm thử đơn vị & kiểm thử kịch bản trực quan theo `quickstart.md`.

**Target Platform**: Microsoft Windows (Windows 10, Windows 11).

**Project Type**: Desktop GUI Application (Clean Architecture 4 tầng).

**Performance Goals**:
- Phản hồi thao tác xoay/lật < 50ms.
- Hiệu ứng chuyển cảnh đạt 60 FPS ổn định, thời lượng tiêu chuẩn 400ms - 500ms.
- Trích xuất luồng âm thanh YouTube trong luồng nền không làm block UI.

**Constraints**: Tuân thủ nghiêm ngặt Hiến pháp dự án: Không import PyQt6 ở tầng Domain và Application; Không phá hủy tệp ảnh gốc; Đảm bảo tương thích đóng gói PyInstaller độc lập.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc / Gate | Đánh Giá Tuân Thủ | Trạng Thái |
|---|---|:---:|
| **I. Clean Architecture & Dependency Rule** | - `MusicPlayerPort`, `BgmConfig`, `ImageTransformState`, `TransitionType` định nghĩa trong `domain/` hoàn toàn bằng Python thuần túy.<br>- `ManageBgmUseCase` nằm trong `application/`.<br>- Triển khai kỹ thuật `YouTubeBgmProvider` nằm trong `infrastructure/`.<br>- `TransitionEngine`, UI Controls nằm trong `presentation/`. | **PASS** |
| **II. Chuẩn Giao Diện PyQt6 & Dark Theme** | Thiết kế nút nhạc nền, thanh trượt âm lượng, nút xoay ảnh và hiệu ứng chuyển cảnh tuân thủ Dark Mode với điểm nhấn Cyan/Teal hiện đại. | **PASS** |
| **III. An Toàn Dữ Liệu & Phục Hồi** | Xoay và lật ảnh là biến đổi đồ họa thuần túy (`QTransform`), tuyệt đối không ghi đè dữ liệu tệp ảnh trên đĩa. Xử lý ngoại lệ mất mạng/link YouTube lỗi không làm crash app. | **PASS** |
| **IV. Tích Hợp Hệ Điều Hành & Ergonomics** | Phím tắt công thái học (`R`, `Shift+R`, `F`, `V`), tự động đảo hướng trượt khi duyệt lùi (Prev), nút BGM truy cập nhanh trên Control Panel. | **PASS** |
| **V. Độc Lập & PyInstaller Readiness** | `yt-dlp` và `PyQt6.QtMultimedia` được kiểm tra tích hợp an toàn; cập nhật `hiddenimports` trong `slideshow.spec` để đóng gói mượt mà. | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/004-bgm-transform-transitions/
├── spec.md                  # Tài liệu đặc tả yêu cầu
├── plan.md                  # Kế hoạch kiến trúc (Tệp này)
├── research.md              # Nghiên cứu giải pháp kỹ thuật yt-dlp & Transition Engine
├── data-model.md            # Mô hình thực thể BgmConfig, TransformState, TransitionType
├── quickstart.md            # Hướng dẫn kiểm thử 3 kịch bản
├── contracts/
│   ├── bgm_service_contract.md       # Hợp đồng cổng phát nhạc & Provider
│   └── transition_engine_contract.md # Hợp đồng bộ điều phối chuyển cảnh Strategy
└── checklists/
    └── requirements.md      # Bảng kiểm định chất lượng đặc tả
```

### Source Code Touchpoints

```text
src/
├── domain/
│   ├── models.py                     # Thêm BgmConfig, ImageTransformState, TransitionType; mở rộng ViewerSettings
│   └── ports.py                      # Thêm MusicPlayerPort
├── application/
│   └── use_cases.py                  # Thêm ManageBgmUseCase, cập nhật ViewerSettings handling
├── infrastructure/
│   ├── bgm/
│   │   ├── __init__.py
│   │   ├── base_provider.py          # Lớp cơ sở trừu tượng Provider
│   │   ├── youtube_provider.py       # Bộ trích xuất và phát nhạc YouTube qua QMediaPlayer & yt-dlp
│   │   └── qt_music_player.py        # Triển khai MusicPlayerPort kết nối các Provider
│   └── json_settings_repo.py         # Bổ sung giá trị mặc định cho các cấu hình mới
└── presentation/
    ├── presenter.py                  # Quản lý transform_cache, điều phối BGM & chuyển cảnh
    └── views/
        ├── transitions/
        │   ├── __init__.py
        │   ├── base_transition.py    # Lớp cơ sở chiến lược hiệu ứng
        │   ├── fade_transition.py    # Hiệu ứng hòa tan Cross-Fade
        │   ├── slide_transition.py   # Hiệu ứng trượt Slide Left / Slide Right có đảo chiều
        │   ├── zoom_transition.py    # Hiệu ứng Zoom Fade
        │   ├── instant_transition.py # Hiệu ứng chuyển cảnh tức thì
        │   └── engine.py             # TransitionEngine đăng ký và thực thi hiệu ứng
        ├── viewer_window.py          # Tích hợp Transform matrix, gọi TransitionEngine, nhận sự kiện phím tắt
        ├── control_panel.py          # Thêm nút BGM (🎵/🔇) và nút Xoay nhanh (🔄)
        └── settings_dialog.py        # Thêm combobox hiệu ứng chuyển cảnh, khu vực cấu hình & nghe thử BGM
slideshow.spec                        # Cập nhật hiddenimports: ['yt_dlp', 'PyQt6.QtMultimedia']
```

**Structure Decision**: Cấu trúc tuân thủ chuẩn Clean Architecture 4 tầng. Tạo module riêng `src/infrastructure/bgm/` cho các bộ phát nhạc và `src/presentation/views/transitions/` cho các chiến lược hiệu ứng chuyển cảnh nhằm đảm bảo tính module hóa và dễ mở rộng tối đa.

## Complexity Tracking

Không có vi phạm hay ngoại lệ so với Hiến pháp dự án.
