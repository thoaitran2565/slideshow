# Implementation Plan: Nâng Cao Độ Rõ Nét & Ghi Nhớ Trạng Thái Thanh Điều Khiển

**Branch**: `002-control-panel-enhancement` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-control-panel-enhancement/spec.md`

## Summary

Nâng cấp độ tương phản thị giác của thanh công cụ điều khiển `ControlPanel` và nút "Hiện thanh công cụ" bằng hiệu ứng `QGraphicsDropShadowEffect` kết hợp giao diện Dark Theme đậm nét `#121212`, viền sáng sắc nét để đảm bảo hiển thị rõ ràng 100% trên các bức ảnh nền trắng/sáng. Mở rộng `ViewerSettings` và `JsonSettingsRepository` để tự động ghi nhớ và khôi phục trạng thái phát ngẫu nhiên (`is_random`) và trạng thái ẩn/hiện (`show_control_panel`) qua các phiên làm việc của người dùng.

## Technical Context

**Language/Version**: Python 3.10+ (PyQt6).

**Primary Dependencies**: `PyQt6` (QtWidgets, QtCore, QtGui, `QGraphicsDropShadowEffect`).

**Storage**: `settings.json` cục bộ quản lý qua `JsonSettingsRepository`.

**Target Platform**: Microsoft Windows (Windows 10, Windows 11).

**Project Type**: Desktop GUI Application.

**Performance Goals**: Đổ bóng mượt mà, phản hồi chuyển trạng thái và lưu cấu hình <20ms, không gây sụt giảm khung hình.

**Constraints**: Tuân thủ tuyệt đối cấu trúc Clean Architecture 4 tầng (Domain thuần túy, Use Case quản lý nghiệp vụ, UI chỉ hiển thị).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc / Gate | Đánh Giá Tuân Thủ | Trạng Thái |
|---|---|---|
| **I. Clean Architecture & Dependency Rule** | Mở rộng `ViewerSettings` trong Domain và `ManageSettingsUseCase` trong Application; không để lọt Qt vào Domain/Application. | **PASS** |
| **II. Chuẩn Giao Diện PyQt6 & Dark Theme** | Sử dụng `QGraphicsDropShadowEffect` và bảng màu Dark tương phản cao, giữ nguyên accent color `#00adb5`. | **PASS** |
| **III. An Toàn Dữ Liệu & Phục Hồi** | Tự động bổ sung giá trị mặc định (`False`, `True`) cho cấu hình cũ, không làm lỗi file JSON. | **PASS** |
| **IV. Tích Hợp Hệ Điều Hành & Ergonomics** | Phím tắt `H` và click chuột mượt mà, ghi nhớ trải nghiệm người dùng liền mạch. | **PASS** |
| **V. Độc Lập & PyInstaller Readiness** | `QGraphicsDropShadowEffect` thuộc sẵn `PyQt6.QtWidgets`, không thêm bất kỳ thư viện ngoài nào. | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/002-control-panel-enhancement/
├── spec.md                  # Tài liệu đặc tả yêu cầu chức năng
├── plan.md                  # Kế hoạch triển khai kiến trúc chi tiết
├── research.md              # Nghiên cứu QGraphicsDropShadowEffect & QSS
├── data-model.md            # Mở rộng ViewerSettings
├── quickstart.md            # Hướng dẫn kiểm thử tương phản & persistence
└── checklists/
    └── requirements.md      # Bảng kiểm định chất lượng đặc tả
```

### Source Code Touchpoints

```text
src/
├── domain/
│   └── models.py                # Bổ sung is_random và show_control_panel vào ViewerSettings
│
├── application/
│   └── use_cases.py             # Bổ sung update_random_state và update_panel_visibility
│
├── infrastructure/
│   └── json_settings_repo.py    # Đọc/ghi is_random và show_control_panel
│
├── presentation/
│   ├── presenter.py             # Đồng bộ trạng thái và lưu cài đặt
│   └── views/
│       ├── control_panel.py     # QSS tương phản cao & QGraphicsDropShadowEffect
│       └── viewer_window.py     # Khôi phục trạng thái khi khởi động, đổ bóng cho btn_show_panel
```

**Structure Decision**: Giữ nguyên kiến trúc Clean Architecture 4 tầng hiện tại, chỉ mở rộng các touchpoints đã được module hóa.

## Complexity Tracking

Không có vi phạm hay ngoại lệ so với Hiến pháp dự án.
