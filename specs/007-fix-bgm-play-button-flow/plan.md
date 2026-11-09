# Implementation Plan: Khắc Phục Luồng Bật Nhạc BGM Trên Thanh Option

**Branch**: `007-fix-bgm-play-button-flow` | **Date**: 2026-11-09 | **Spec**: [spec.md](file:///d:/Code/apps/slideshow_app/specs/007-fix-bgm-play-button-flow/spec.md)

**Input**: Feature specification from `/specs/007-fix-bgm-play-button-flow/spec.md`

## Summary

Khắc phục triệt để hai vấn đề khi thao tác nút Bật/Tắt nhạc nền (BGM) trên thanh công cụ option:
1. **Vấn đề 1**: Khắc phục lỗi bấm nút BGM ở màn hình chính vẫn mở Cài đặt dù đã có link nhạc được thiết lập (do phụ thuộc vào cờ boolean cũ `bgm_enabled: false` trong `settings.json`).
2. **Vấn đề 2**: Khắc phục lỗi vừa mở ứng dụng lên bấm Bật nhạc thì không có phản ứng hay loading gì (do `ManageBgmUseCase.play()` chỉ gọi `play()` trên player chưa nạp source, buộc người dùng phải vào Cài đặt bấm "Nghe thử" trước đó để mồi source).

Giải pháp:
- Sửa `is_bgm_ready()` trong `src/presentation/presenter.py` chỉ phụ thuộc vào tính hợp lệ của chuỗi `bgm_youtube_url`.
- Cải tiến `ManageBgmUseCase.play()` trong `src/application/use_cases.py` để tự động kiểm tra và gọi `music_player.set_source(url)` nếu `current_target` chưa được nạp hoặc khác với URL cấu hình hiện tại.

---

## Technical Context

**Language/Version**: Python 3.10 - 3.14 (UTF-8 encoding)  
**Primary Dependencies**: PyQt6 (GUI, QMediaPlayer), yt-dlp (YouTube stream resolution)  
**Storage**: JSON (`settings.json` qua `JsonSettingsRepository`)  
**Testing**: PyQt6 pytest/unittest script chạy trực tiếp (`tests/test_feature_007.py`)  
**Target Platform**: Microsoft Windows 10/11  
**Project Type**: Desktop GUI Application (Photo Viewer with Slideshow & Background Music)  
**Performance Goals**: Nút bấm phản hồi tức thì (< 50ms), chuyển ngay sang trạng thái "⏳ Đang tải..."  
**Constraints**: Tuân thủ Clean Architecture 4 tầng; Domain/Application không import PyQt6; tương thích đóng gói PyInstaller single-exe  
**Scale/Scope**: Ảnh hưởng đến 2 file lõi: `src/presentation/presenter.py` và `src/application/use_cases.py`, cùng kiểm thử `tests/test_feature_007.py`.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc Hiến Pháp | Tình Trạng | Đánh Giá Tuân Thủ |
|---|---|---|
| **I. Clean Architecture & Dependency Rule** | ✅ PASS | Logic nạp nguồn tự động được xử lý tại `ManageBgmUseCase` (Tầng Application) thông qua `MusicPlayerPort` trừu tượng, không import PyQt6. Logic kiểm tra sẵn sàng giao diện nằm ở `Presenter` (Tầng Presentation). |
| **II. Native UI/UX & Dark Theme** | ✅ PASS | Trạng thái nút BGM giữ nguyên chuẩn Dark Theme, phản hồi trạng thái rõ ràng ("⏳ Đang tải...", "⏸ Tắt nhạc", "🎵 Bật nhạc"). |
| **III. Safe Operations & Data Resilience** | ✅ PASS | Xử lý URL rỗng an toàn, dự phòng trường hợp `settings.json` mang cờ cũ không gây crash hoặc hành vi sai. |
| **IV. System Integration & Ergonomics** | ✅ PASS | Loại bỏ thao tác thừa, người dùng bấm 1 chạm là nghe nhạc ngay lập tức. |
| **V. PyInstaller Readiness** | ✅ PASS | Không thêm thư viện ngoài mới, hoàn toàn tương thích với file đặc tả `slideshow.spec`. |

---

## Project Structure

### Documentation (this feature)

```text
specs/007-fix-bgm-play-button-flow/
├── plan.md              # Kế hoạch triển khai kiến trúc (file này)
├── research.md          # Phân tích nguyên nhân gốc rễ & giải pháp kỹ thuật
├── data-model.md        # Mô hình dữ liệu & vòng đời trạng thái BGM
├── quickstart.md        # Hướng dẫn kiểm thử thủ công và tự động
├── contracts/           # Đặc tả interface & hành vi các tầng
│   └── bgm_play_fix_contract.md
├── checklists/
│   └── requirements.md  # Checklist tiêu chí kỹ thuật
└── tasks.md             # Sẽ được tạo bởi lệnh /speckit-tasks
```

### Source Code (repository root)

```text
src/
├── domain/                      # Tầng 1: Models & Ports (0 Qt dependency)
│   ├── models.py                # BgmPlaybackState, ViewerSettings, BgmConfig
│   └── ports.py                 # MusicPlayerPort, SettingsRepositoryPort
├── application/                 # Tầng 2: Use Cases
│   └── use_cases.py             # ManageBgmUseCase (SỬA: tự động gọi set_source)
├── infrastructure/              # Tầng 3: Repositories & Adapters
│   ├── json_settings_repo.py    # Đồng bộ bgm_enabled an toàn
│   └── qt_music_player.py       # Triển khai MusicPlayerPort
├── presentation/                # Tầng 4: Presenter & Views PyQt6
│   ├── presenter.py             # Presenter (SỬA: is_bgm_ready chỉ check url)
│   └── views/
│       └── viewer_window.py     # toggle_bgm_action
tests/
└── test_feature_007.py          # Script kiểm thử tự động tính năng 007
```

**Structure Decision**: Giữ nguyên kiến trúc Clean Architecture hiện tại, chỉ can thiệp vào các phương thức cụ thể đã xác định để giải quyết triệt để 2 vấn đề mà không gây phản ứng phụ.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*(Không có vi phạm nào đối với Hiến pháp dự án)*
