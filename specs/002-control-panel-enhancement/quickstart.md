# Quickstart & Verification Guide: Control Panel Enhancement

**Feature**: `002-control-panel-enhancement`  
**Date**: 2026-11-09  
**Status**: Ready for Implementation  

---

## 1. Kịch Bản Kiểm Thử Thị Giác (Visual Contrast Test)

1. Mở ứng dụng với một ảnh có nền trắng hoặc rất sáng:
   ```powershell
   python main.py
   ```
2. Quan sát thanh `ControlPanel` ở đáy màn hình:
   - Thanh panel có viền sáng rõ nét và bóng đổ đen mịn màng bao quanh.
   - Toàn bộ các nút Play/Pause, Random, Nền, nút +/- và nhãn tốc độ đọc rõ 100%, không bị chìm hay mờ lóa.
3. Bấm nút "Ẩn" (hoặc phím `H`) để ẩn thanh công cụ:
   - Nút "👁️ Hiện thanh công cụ" xuất hiện ở giữa đáy màn hình với bóng đổ và viền sáng rõ nét trên nền ảnh trắng.

---

## 2. Kịch Bản Kiểm Thử Ghi Nhớ Chế Độ Random (Random Persistence Test)

1. Mở app, bấm vào nút "🔀 Random" để kích hoạt (nút đổi màu sáng/active).
2. Tắt ứng dụng.
3. Mở lại ứng dụng:
   ```powershell
   python main.py
   ```
4. Xác nhận:
   - Nút "🔀 Random" vẫn ở trạng thái được chọn (checked).
   - Nhãn góc trên bên trái hiển thị `🔀 Random - <tên file>`.
   - Bấm duyệt ảnh tiếp theo phát theo thứ tự ngẫu nhiên.

---

## 3. Kịch Bản Kiểm Thử Ghi Nhớ Ẩn/Hiện Thanh Công Cụ (Visibility Persistence Test)

1. Mở app, bấm nút "👁️ Ẩn" (hoặc phím `H`): thanh công cụ ẩn đi, nút "👁️ Hiện thanh công cụ" xuất hiện.
2. Tắt ứng dụng.
3. Mở lại ứng dụng:
   ```powershell
   python main.py
   ```
4. Xác nhận:
   - Ứng dụng khởi động với thanh công cụ vẫn ẩn sẵn.
   - Nút "👁️ Hiện thanh công cụ" hiển thị sẵn sàng ở góc dưới màn hình.
   - Nhấp vào nút "Hiện thanh công cụ": thanh công cụ mở ra bình thường.

