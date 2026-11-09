# Implementation Plan: Giới Hạn Mức Thu Nhỏ Tối Thiểu (Chỉ Cho Phép Phóng To Chi Tiết)

**Branch**: `003-restrict-min-zoom` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/003-restrict-min-zoom/spec.md`

## Summary

Kiểm soát chặt chẽ tỷ lệ phóng đại (Zoom Ratio) trong `PhotoViewerWindow` của tầng Presentation: xác lập mức hiển thị vừa khít cửa sổ (`fitInView`) làm mốc cơ sở $1.0x$. Cho phép người dùng cuộn chuột lên để phóng to chi tiết ảnh (lên tới $20.0x$), nhưng chặn hoàn toàn (clamp) thao tác cuộn chuột xuống nếu ảnh đã ở kích thước cơ sở $1.0x$, loại bỏ triệt để hiện tượng ảnh bị thu nhỏ thành chấm li ti. Tự động reset tỷ lệ zoom về $1.0x$ khi chuyển ảnh hoặc resize cửa sổ.

## Technical Context

**Language/Version**: Python 3.10+ (PyQt6).

**Primary Dependencies**: `PyQt6` (`QGraphicsView`, `QGraphicsScene`, `QGraphicsPixmapItem`).

**Target Platform**: Microsoft Windows (Windows 10, Windows 11).

**Project Type**: Desktop GUI Application.

**Performance Goals**: Phản hồi cuộn chuột tức thời (60 FPS), không giật khung hình khi kẹp giá trị zoom.

**Constraints**: Tuân thủ tuyệt đối kiến trúc Clean Architecture; toàn bộ logic zoom nằm gọn trong Presentation View, không xâm lấn tầng Domain hay Application.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Nguyên Tắc / Gate | Đánh Giá Tuân Thủ | Trạng Thái |
|---|---|---|
| **I. Clean Architecture & Dependency Rule** | Logic zoom là chi tiết điều phối tương tác UI của `PhotoViewerWindow`, không vi phạm ranh giới Domain/Application. | **PASS** |
| **II. Chuẩn Giao Diện PyQt6 & Dark Theme** | Giữ trọn vẹn canvas `QGraphicsView` và trải nghiệm zoom/pan mượt mà của PyQt6. | **PASS** |
| **III. An Toàn Dữ Liệu & Phục Hồi** | Không tác động đến dữ liệu tệp tin hay cấu hình hệ thống. | **PASS** |
| **IV. Tích Hợp Hệ Điều Hành & Ergonomics** | Cải thiện công thái học thao tác chuột cho người dùng Windows. | **PASS** |
| **V. Độc Lập & PyInstaller Readiness** | Sử dụng API có sẵn của `PyQt6.QtWidgets`, không thêm thư viện ngoài. | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/003-restrict-min-zoom/
├── spec.md                  # Tài liệu đặc tả yêu cầu chức năng
├── plan.md                  # Kế hoạch triển khai kiến trúc chi tiết
├── research.md              # Nghiên cứu giải pháp tỷ lệ tương đối QGraphicsView
├── data-model.md            # Mô hình trạng thái ZoomState
├── quickstart.md            # Hướng dẫn kiểm thử 3 kịch bản zoom
└── checklists/
    └── requirements.md      # Bảng kiểm định chất lượng đặc tả
```

### Source Code Touchpoints

```text
src/
└── presentation/
    └── views/
        └── viewer_window.py # Triển khai self.current_zoom, fit_image_in_view() reset,
                             # và thuật toán kẹp giá trị clamp trong wheelEvent()
```

**Structure Decision**: Cập nhật trực tiếp tệp `src/presentation/views/viewer_window.py`.

## Complexity Tracking

Không có vi phạm hay ngoại lệ so với Hiến pháp dự án.
