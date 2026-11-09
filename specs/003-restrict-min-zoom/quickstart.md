# Quickstart & Verification Guide: Restrict Min Zoom

**Feature**: `003-restrict-min-zoom`  
**Date**: 2026-11-09  
**Status**: Ready for Implementation  

---

## 1. Kịch Bản Kiểm Thử Chặn Thu Nhỏ Tại Kích Thước Gốc (No Zoom-Out Below Fit)

1. Mở ứng dụng:
   ```powershell
   python main.py
   ```
2. Ảnh đầu tiên được hiển thị vừa khít cửa sổ (`Fit in View`).
3. Thực hiện cuộn con lăn chuột xuống (Scroll Down) liên tục 5-10 lần:
   - **Kết quả kỳ vọng**: Ảnh vẫn giữ nguyên kích thước đầy đủ vừa khít cửa sổ, tuyệt đối không bị thu nhỏ lại hay xuất hiện khoảng đen thừa bao quanh ảnh.

---

## 2. Kịch Bản Kiểm Thử Phóng To & Thu Nhỏ Quay Về Ngưỡng Gốc

1. Cuộn chuột lên (Scroll Up) 3 lần:
   - **Kết quả kỳ vọng**: Ảnh phóng to dần, cho phép giữ chuột trái kéo ảnh (Pan) để xem các góc khuất.
2. Cuộn chuột xuống (Scroll Down) 5 lần:
   - **Kết quả kỳ vọng**: Ảnh thu nhỏ dần lại; khi về đến đúng kích thước ban đầu thì dừng lại hoàn toàn và tự động căn giữa khung nhìn.

---

## 3. Kịch Bản Kiểm Thử Reset Zoom Khi Chuyển Ảnh & Đổi Cửa Sổ

1. Khi đang ở trạng thái phóng to một bức ảnh:
   - Bấm phím mũi tên Phải (`Right Arrow`) để chuyển sang ảnh tiếp theo.
   - **Kết quả kỳ vọng**: Ảnh mới được nạp lập tức ở trạng thái vừa khít khung nhìn ($1.0x$) và không bị lưu vết tỷ lệ phóng to của ảnh cũ.
2. Bấm phím `F11` để chuyển đổi chế độ Toàn màn hình:
   - **Kết quả kỳ vọng**: Ảnh tự động căn chỉnh vừa khít kích thước toàn màn hình mới ở mốc $1.0x$.

