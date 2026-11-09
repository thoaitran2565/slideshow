# Implementation Plan: Nâng Cấp Điều Khiển Nhạc Nền (Live Volume, Quick Popup, BGM Label & Source Protection)

**Branch**: `005-bgm-controls-enhancement` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-bgm-controls-enhancement/spec.md`

## Summary

Triển khai gói 4 cải tiến công thái học và điều khiển âm thanh nhạc nền:
1. **Cập nhật âm lượng thời gian thực (Live Volume)**: Kết nối sự kiện `valueChanged` của thanh trượt âm lượng trực tiếp tới `manage_bgm_uc.set_volume(val)` trong cả hộp thoại Cài đặt (khi "Nghe thử") và trong lúc xem slideshow.
2. **Popup chỉnh âm lượng nhanh bằng chuột phải (Quick Volume Popup)**: Bắt sự kiện chuột phải trên nút BGM của thanh `ControlPanel` để mở widget popup nổi không viền, cho phép chỉnh âm thanh trực tiếp và tự động lưu.
3. **Chuẩn hóa nhãn nút BGM**: Đổi nhãn nút thành `"🎵 Bật nhạc"` (khi tắt) và `"🔇 Tắt nhạc"` (khi bật) kèm tooltip công thái học; nới rộng kích thước thanh điều khiển nổi để hiển thị hoàn hảo.
4. **Bảo vệ chọn nguồn phát nhạc**: Vô hiệu hóa (disable) các mục chưa hỗ trợ ("Spotify", "Tệp ổ cứng cục bộ") trong ComboBox của `SettingsDialog`, ngăn chặn người dùng chọn nhầm.

## Technical Context

**Language/Version**: Python 3.10+ (PyQt6 6.4+).

**Primary Dependencies**: `PyQt6` (`QtWidgets`, `QtGui`, `QtCore`, `QtMultimedia`).

**Storage**: Tệp cấu hình JSON duy nhất `settings.json` thông qua `JsonSettingsRepository`.

**Testing**: Kiểm thử đơn vị & kiểm thử kịch bản trực quan theo `quickstart.md`.

**Target Platform**: Microsoft Windows (Windows 10, Windows 11).

**Project Type**: Desktop GUI Application (Clean Architecture 4 tầng).

**Performance Goals**:
- Phản hồi điều chỉnh âm lượng tức thì ra loa < 50ms.
- Popup âm lượng hiển thị ngay lập tức (< 100ms) không gây giật lag giao diện.
- Không ghi đĩa lặp lại liên tục khi kéo chuột (chỉ lưu vào `settings.json` khi kết thúc thao tác hoặc đóng popup/dialog).

**Constraints**: Tuân thủ nghiêm ngặt Hiến pháp dự án: Không import PyQt6 ở tầng Domain và Application; Giữ vững bố cục Dark Theme đồng nhất.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc / Gate | Đánh Giá Tuân Thủ | Trạng Thái |
|---|---|:---:|
| **I. Clean Architecture & Dependency Rule** | - Logic điều khiển âm lượng và cập nhật cấu hình tuân thủ luồng: Presenter -> Use Case -> Port -> QtMusicPlayer.<br>- Không import PyQt6 ở Domain và Application. | **PASS** |
| **II. Chuẩn Giao Diện PyQt6 & Dark Theme** | `QuickVolumePopup` thiết kế theo phong cách Dark Theme bo tròn góc với viền nhấn Cyan (`#00adb5`) đồng bộ với `ControlPanel`. | **PASS** |
| **III. An Toàn Dữ Liệu & Phục Hồi** | Tối ưu hóa ghi cấu hình đĩa (`settings.json`) khi thả chuột, cơ chế fallback defaults luôn đảm bảo an toàn. | **PASS** |
| **IV. Tích Hợp Hệ Điều Hành & Ergonomics** | Thao tác chuột phải mở volume control tương tự như taskbar Windows, nhãn nút "Bật nhạc" / "Tắt nhạc" rõ ràng. | **PASS** |
| **V. Độc Lập & PyInstaller Readiness** | Sử dụng toàn bộ thành phần chuẩn PyQt6 đã được tích hợp trong dự án, tương thích hoàn toàn khi đóng gói `Slideshow.exe`. | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/005-bgm-controls-enhancement/
├── spec.md                  # Đặc tả yêu cầu người dùng
├── plan.md                  # Kế hoạch kiến trúc (Tệp này)
├── research.md              # Nghiên cứu kỹ thuật Live Volume & Popup
├── data-model.md            # Mô hình thực thể và trạng thái UI
├── quickstart.md            # Hướng dẫn kiểm thử 4 kịch bản
├── contracts/
│   └── bgm_controls_contract.md  # Hợp đồng giao tiếp UI & Presenter
└── checklists/
    └── requirements.md      # Bảng kiểm định chất lượng đặc tả
```

### Source Code Touchpoints

```text
src/
├── presentation/
│   ├── presenter.py                  # Thêm set_bgm_volume(val, persist) và persist_bgm_volume(val)
│   └── views/
│       ├── control_panel.py          # Thêm QuickVolumePopup, bắt sự kiện chuột phải trên btn_bgm, cập nhật nhãn 'Bật nhạc' / 'Tắt nhạc'
│       ├── settings_dialog.py        # Kết nối valueChanged của slider_bgm_volume thời gian thực, vô hiệu hóa các item chưa hỗ trợ trong cmb_bgm_source
│       └── viewer_window.py          # Đấu nối tín hiệu volume từ ControlPanel vào Presenter, nới rộng panel_width = 760
```

## Complexity Tracking

Không có vi phạm hay ngoại lệ so với Hiến pháp dự án.
