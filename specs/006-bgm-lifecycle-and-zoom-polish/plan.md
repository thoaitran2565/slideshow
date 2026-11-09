# Implementation Plan: Tinh Chỉnh Vòng Đời Nhạc Nền, Lớp Phủ Chống Click Xuyên & Tối Ưu Mượt Mà Hiệu Ứng Zoom Fade

**Branch**: `006-bgm-lifecycle-and-zoom-polish` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/006-bgm-lifecycle-and-zoom-polish/spec.md`

## Summary

Triển khai gói 4 cải tiến tinh tế về vòng đời BGM, an toàn giao diện và độ mượt mà đồ họa:
1. **Độc lập vòng đời BGM & Ngăn ngừa xung đột**: Tách rời hoàn toàn lệnh Tạm dừng/Tiếp tục của trình chiếu khỏi nhạc nền; loại bỏ ô checkbox kích hoạt trong Cài đặt; tự động ngắt nhạc nền slideshow khi sửa link hoặc bấm nghe thử trong Cài đặt.
2. **Trạng thái nạp nhạc BGM (Loading) & Safety Timeout (15s)**: Chuyển nút BGM sang `"⏳ Đang tải..."` và khóa click chống spam; tab Cài đặt hiển thị loading; cài đặt `QTimer` 15 giây tự động hủy luồng và thông báo lỗi nhẹ nhàng nếu quá thời gian hoặc lỗi mạng.
3. **Lớp phủ chống click xuyên (Transparent Modal Backdrop Overlay)**: Chặn sự kiện click xuyên thấu khi đóng Quick Volume Popup bằng lớp phủ trong suốt, đảm bảo cú click ra ngoài chỉ đóng thanh âm lượng mà không vô tình kích hoạt các nút bên dưới.
4. **Chuẩn hóa mượt mà hiệu ứng Zoom Fade**: Tiền xử lý tỉ lệ chuẩn hóa (`fitInView`) cho ảnh mới trước khi hòa trộn, đồng tâm và mượt mà ở 60 FPS, chấm dứt hiện tượng giật nảy khung hình khi chuyển đổi giữa các ảnh chênh lệch kích thước.

## Technical Context

**Language/Version**: Python 3.10+ (PyQt6 6.4+).

**Primary Dependencies**: `PyQt6` (`QtWidgets`, `QtGui`, `QtCore`, `QtMultimedia`), `yt-dlp`.

**Storage**: Tệp cấu hình JSON duy nhất `settings.json` thông qua `JsonSettingsRepository`.

**Testing**: Kiểm thử đơn vị & kiểm thử kịch bản trực quan theo `quickstart.md`.

**Target Platform**: Microsoft Windows (Windows 10, Windows 11).

**Project Type**: Desktop GUI Application (Clean Architecture 4 tầng).

**Performance Goals**:
- Hoạt ảnh Zoom Fade đạt 60 FPS ổn định, không giật nảy.
- Nút BGM chuyển trạng thái Loading < 30ms sau khi bấm.
- Timeout giới hạn 15 giây chính xác và dọn dẹp luồng an toàn.

**Constraints**: Tuân thủ nghiêm ngặt Hiến pháp dự án: Không import PyQt6 ở tầng Domain và Application; Giữ vững giao diện Dark Theme đồng bộ.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc / Gate | Đánh Giá Tuân Thủ | Trạng Thái |
|---|---|:---:|
| **I. Clean Architecture & Dependency Rule** | - `BgmPlaybackState` định nghĩa tại Domain/Application.<br>- Quản lý timeout và thread extraction nằm trong Infrastructure.<br>- Lớp phủ và Transition nằm trong Presentation. | **PASS** |
| **II. Chuẩn Giao Diện PyQt6 & Dark Theme** | Giữ vững Dark Theme đồng bộ, trạng thái Loading rõ ràng, viền Cyan `#00adb5`. | **PASS** |
| **III. An Toàn Dữ Liệu & Phục Hồi** | Hủy luồng an toàn khi timeout hoặc đóng app, không gây leak tài nguyên hay crash ứng dụng. | **PASS** |
| **IV. Tích Hợp Hệ Điều Hành & Ergonomics** | Lớp phủ trong suốt chống click xuyên bảo vệ an toàn cho thao tác người dùng. | **PASS** |
| **V. Độc Lập & PyInstaller Readiness** | Sử dụng toàn bộ thư viện chuẩn đã có, tương thích đóng gói `Slideshow.exe`. | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/006-bgm-lifecycle-and-zoom-polish/
├── spec.md                  # Đặc tả yêu cầu người dùng
├── plan.md                  # Kế hoạch kiến trúc (Tệp này)
├── research.md              # Nghiên cứu kỹ thuật Loading & Zoom Fade
├── data-model.md            # Mô hình thực thể và trạng thái UI
├── quickstart.md            # Hướng dẫn kiểm thử 4 kịch bản
├── contracts/
│   └── bgm_lifecycle_contract.md # Hợp đồng giao tiếp Loading & Overlay
└── checklists/
    └── requirements.md      # Bảng kiểm định chất lượng đặc tả
```

### Source Code Touchpoints

```text
src/
├── domain/
│   └── models.py                     # Thêm BgmPlaybackState
├── infrastructure/
│   └── bgm/
│       └── qt_music_player.py        # Thêm QTimer 15s safety timeout, quản lý BgmPlaybackState, cancel_loading()
├── presentation/
│   ├── presenter.py                  # Tách rời slideshow pause/play khỏi BGM, truyền callback trạng thái playback
│   └── views/
│       ├── control_panel.py          # Thêm BackdropOverlay chống click xuyên, hàm set_bgm_loading()
│       ├── settings_dialog.py        # Loại bỏ chk_bgm_enable, tự ngắt BGM khi gõ url/nghe thử, hiển thị loading state
│       ├── transitions/
│       │   └── zoom_transition.py    # Tiền tính toán tỉ lệ fit trước khi hòa trộn, mượt mà 60 FPS
│       └── viewer_window.py          # Tách rời toggle_play_pause khỏi BGM, kích hoạt overlay khi mở popup
```

## Complexity Tracking

Không có vi phạm hay ngoại lệ so với Hiến pháp dự án.
