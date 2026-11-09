# Implementation Plan: Tái Cấu Trúc Dự Án Theo Clean Architecture

**Branch**: `001-clean-architecture-refactor` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-clean-architecture-refactor/spec.md`

## Summary

Tái cấu trúc toàn bộ mã nguồn ứng dụng trình chiếu ảnh hiện tại sang mô hình **Clean Architecture 4 tầng**: tách biệt hoàn toàn giữa tầng logic nghiệp vụ (`Domain`, `Application`) và tầng hiển thị/hệ thống (`Presentation`, `Infrastructure`). Hợp nhất việc quản lý cấu hình về duy nhất `settings.json`, dọn dẹp các tệp dư thừa (`config_manager.py`), đảm bảo 100% không hồi quy tính năng (zero regression) và giữ trọn vẹn khả năng đóng gói PyInstaller độc lập thành `Slideshow.exe`.

## Technical Context

**Language/Version**: Python 3.10+ (đang chạy trên môi trường Windows).

**Primary Dependencies**: `PyQt6` (Widgets, GraphicsView, Core, Gui), `send2trash` (Thao tác thùng rác an toàn), `PyInstaller` (Đóng gói tệp thực thi).

**Storage**: Tệp JSON cục bộ (`settings.json`) mã hóa UTF-8 với fallback mặc định an toàn.

**Testing**: Kiểm thử độc lập từng tầng (Unit Testing tầng Domain/Application không cần Qt; Integration Testing cho GUI & PyInstaller build).

**Target Platform**: Microsoft Windows (Windows 10, Windows 11).

**Project Type**: Desktop GUI Application (Single Executable Windows App).

**Performance Goals**: Thời gian nạp khởi động và thời gian chuyển ảnh <100ms; không đóng băng giao diện khi quét thư mục.

**Constraints**: Không dùng thêm framework ngoài; mã nguồn thuần túy Python + PyQt6; duy trì toàn bộ phím tắt và hành vi xem ảnh hiện tại.

**Scale/Scope**: Tái cấu trúc toàn diện 8 module hiện có trong `src/` thành cấu trúc Clean Architecture chuẩn hóa.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc / Gate | Đánh Giá Tuân Thủ | Trạng Thái |
|---|---|---|
| **I. Phân Tách Trách Nhiệm** | Tách bạch rõ rệt 4 tầng: Domain (không phụ thuộc), Application (Use Cases), Infrastructure (Repositories/Adapters), Presentation (PyQt6 Views & Presenter). | **PASS** |
| **II. Chuẩn Giao Diện PyQt6 & Dark Theme** | Giữ nguyên 100% giao diện Dark Mode tương phản cao, màu Cyan `#00adb5`, canvas `QGraphicsView` zoom/pan mượt mà và đa màn hình. | **PASS** |
| **III. An Toàn Dữ Liệu & Phục Hồi** | Xóa ảnh qua `send2trash` kèm xác nhận hộp thoại; fallback cấu hình mặc định an toàn chống crash. | **PASS** |
| **IV. Tích Hợp Hệ Điều Hành & Ergonomics** | Duy trì Registry Open With (`winreg`), tham số dòng lệnh `sys.argv[1]`, AppUserModelID cho taskbar và Windows Natural Sort. | **PASS** |
| **V. Độc Lập & Sẵn Sàng PyInstaller** | Không phát sinh thư viện bên ngoài nặng; cấu hình `slideshow.spec` được đồng bộ để build `.exe` một tệp duy nhất. | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/001-clean-architecture-refactor/
├── spec.md                  # Tài liệu đặc tả yêu cầu chức năng
├── plan.md                  # Kế hoạch triển khai kiến trúc chi tiết
├── research.md              # Báo cáo nghiên cứu mô hình Clean Architecture
├── data-model.md            # Mô hình thực thể Domain và Ports
├── quickstart.md            # Hướng dẫn kiểm thử và xác thực
├── contracts/               # Hợp đồng Use Cases và Presentation View
│   ├── use_case_contracts.md
│   └── presentation_view_contracts.md
└── checklists/
    └── requirements.md      # Bảng kiểm định chất lượng đặc tả
```

### Source Code (repository root)

```text
src/
├── domain/                      # TẦNG 1: DOMAIN (Core Business Rules)
│   ├── __init__.py
│   ├── models.py                # ImageItem, Playlist, ViewerSettings
│   └── ports.py                 # ImageRepositoryPort, SettingsRepositoryPort, SystemPort
│
├── application/                 # TẦNG 2: USE CASES (Application Business Rules)
│   ├── __init__.py
│   ├── use_cases.py             # LoadImagesUseCase, NavigatePlaylistUseCase,
│   │                            # DeleteImageUseCase, ManageFavoritesUseCase,
│   │                            # ManageSettingsUseCase
│   └── sorting.py               # Thuật toán Windows Natural Sort tách biệt
│
├── infrastructure/              # TẦNG 3: INFRASTRUCTURE / ADAPTERS
│   ├── __init__.py
│   ├── json_settings_repo.py    # Đọc/ghi settings.json với fallback an toàn
│   ├── local_image_repo.py      # Quét file qua glob, xóa file qua send2trash
│   ├── windows_system_adapter.py# Tích hợp Windows Registry, ctypes AppUserModelID
│   └── path_utils.py            # Xử lý đường dẫn tệp khi chạy dev vs đóng gói frozen exe
│
├── presentation/                # TẦNG 4: PRESENTATION (PyQt6 UI)
│   ├── __init__.py
│   ├── presenter.py             # ViewerPresenter kết nối Use Cases với View
│   └── views/
│       ├── __init__.py
│       ├── viewer_window.py     # Cửa sổ chính PhotoViewerWindow (QGraphicsView)
│       ├── control_panel.py     # ControlPanel widget Dark Theme
│       ├── splash_screen.py     # CustomSplashScreen đa màn hình
│       ├── settings_dialog.py   # SettingsDialog cấu hình
│       └── favorites_window.py  # FavoritesWindow bộ sưu tập ảnh
│
├── assets/
│   └── app_icon.ico             # Biểu tượng ứng dụng
│
├── config.py                    # Cầu nối tương thích ngược (Forwarding shim sang infra)
└── __init__.py

main.py                          # Composition Root: Khởi tạo DI, nạp argv, chạy app
slideshow.spec                   # Kịch bản đóng gói PyInstaller
settings.json                    # Cấu hình người dùng duy nhất
```

**Structure Decision**: Lựa chọn kiến trúc Single Project đa tầng (Clean Architecture) phân định rõ ranh giới phụ thuộc: Presentation và Infrastructure phụ thuộc vào Application và Domain; Domain không phụ thuộc vào bất kỳ tầng nào khác.

## Complexity Tracking

Không có vi phạm hay ngoại lệ so với Hiến pháp dự án. Toàn bộ thiết kế bám sát chặt chẽ các nguyên tắc cốt lõi đã đề ra.
