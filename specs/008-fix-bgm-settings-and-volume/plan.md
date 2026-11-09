# Implementation Plan: Tinh Chỉnh Vòng Đời BGM Trong Cài Đặt & Khởi Tạo Âm Lượng

**Branch**: `008-fix-bgm-settings-and-volume` | **Date**: 2026-11-09 | **Spec**: [spec.md](file:///d:/Code/apps/slideshow_app/specs/008-fix-bgm-settings-and-volume/spec.md)

**Input**: Feature specification from `/specs/008-fix-bgm-settings-and-volume/spec.md`

## Summary

Giải quyết triệt để 3 vấn đề liên quan đến vòng đời nhạc nền và khởi tạo âm lượng:
1. **Đóng/Hủy Cài đặt làm tắt nhạc nền**: Sửa logic trong `SettingsDialog` để chỉ gọi `manage_bgm_uc.stop()` khi người dùng thực sự đang ở chế độ Nghe thử (`is_testing_audio == True`).
2. **Lưu Cài đặt ngắt nhạc dù không đổi link**: Lưu vết `initial_youtube_url` và `initial_bgm_source`; chỉ dừng và nạp lại nguồn khi các thông số này có sự thay đổi thực tế khi nhấn "Lưu".
3. **Âm lượng khởi động sai lệch**: Bổ sung lệnh khởi tạo âm lượng `music_player.set_volume(settings.bgm_volume)` trong `main.py` và bảo đảm đồng bộ trong `ManageBgmUseCase.play()`.

---

## Technical Context

**Language/Version**: Python 3.10 - 3.14 (UTF-8 encoding)  
**Primary Dependencies**: PyQt6 (GUI, QMediaPlayer, QAudioOutput), yt-dlp  
**Storage**: JSON (`settings.json` qua `JsonSettingsRepository`)  
**Testing**: PyQt6 pytest/unittest script (`tests/test_feature_008.py`)  
**Target Platform**: Microsoft Windows 10/11  
**Project Type**: Desktop GUI Application  
**Performance Goals**: Đóng Cài đặt và Lưu Cài đặt phản hồi tức thời (< 30ms), không giật ngắt luồng audio  
**Constraints**: Tuân thủ Clean Architecture 4 tầng, Domain/Application cấm import PyQt6, tương thích đóng gói PyInstaller  
**Scale/Scope**: Tác động đến 3 tệp tin chính: `main.py`, `src/presentation/views/settings_dialog.py`, và `src/application/use_cases.py`.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc Hiến Pháp | Tình Trạng | Đánh Giá Tuân Thủ |
|---|---|---|
| **I. Clean Architecture & Dependency Rule** | ✅ PASS | Logic nghiệp vụ BGM và đồng bộ âm lượng nằm ở `ManageBgmUseCase` (Application), `MusicPlayerPort` (Domain). Logic giao diện dialog nằm ở Presentation. |
| **II. Native UI/UX & Dark Theme** | ✅ PASS | Trải nghiệm người dùng liền mạch, nhạc không bị tắt oan uổng khi thao tác các cài đặt khác. |
| **III. Safe Operations & Data Resilience** | ✅ PASS | Mức âm lượng được nạp và lưu an toàn qua `settings.json`, có fallback an toàn. |
| **IV. System Integration & Ergonomics** | ✅ PASS | Hỗ trợ phím Esc để đóng Cài đặt mà không làm ngắt nhạc nền. |
| **V. PyInstaller Readiness** | ✅ PASS | Không thêm thư viện phụ thuộc mới, tương thích 100% với `slideshow.spec`. |

---

## Project Structure

### Documentation (this feature)

```text
specs/008-fix-bgm-settings-and-volume/
├── plan.md              # Kế hoạch triển khai kiến trúc
├── research.md          # Phân tích nguyên nhân & giải pháp kỹ thuật
├── data-model.md        # Mô hình trạng thái và vòng đời BGM
├── quickstart.md        # Hướng dẫn kiểm thử thủ công và tự động
├── contracts/           # Đặc tả interface contract
│   └── bgm_lifecycle_volume_contract.md
├── checklists/
│   └── requirements.md  # Checklist chất lượng yêu cầu
└── tasks.md             # Sẽ được tạo bởi lệnh /speckit-tasks
```

### Source Code (repository root)

```text
main.py                                  # Composition Root: Khởi tạo âm lượng từ settings
src/
├── application/
│   └── use_cases.py                     # ManageBgmUseCase: play() đồng bộ volume, apply_settings_without_reload
├── presentation/
│   ├── presenter.py                     # Điều phối BGM config update
│   └── views/
│       └── settings_dialog.py           # Sửa reject(), stop_test_audio(), save_data()
tests/
└── test_feature_008.py                  # Script kiểm thử tự động tính năng 008
```

---

## Complexity Tracking

*(Không có vi phạm nào đối với Hiến pháp dự án)*
