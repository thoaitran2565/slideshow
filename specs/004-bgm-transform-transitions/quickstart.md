# Quickstart & Verification Guide: BGM, Transform & Transitions

**Feature**: `004-bgm-transform-transitions`  
**Date**: 2026-11-09  
**Status**: Ready for Planning / Implementation  

---

## 1. Kịch Bản Kiểm Thử Nhạc Nền YouTube (BGM Verification)

1. **Khởi chạy ứng dụng**:
   ```powershell
   python main.py
   ```
2. **Kiểm tra nút BGM trên thanh điều khiển (Control Panel)**:
   - Nhấn nút 🎵 trên thanh điều khiển.
   - **Kỳ vọng**: Vì chưa cấu hình URL nhạc ban đầu, ứng dụng tự động bật mở hộp thoại Cài đặt (SettingsDialog).
3. **Cấu hình & Nghe thử trong Cài đặt**:
   - Tích chọn "Bật nhạc nền".
   - Dán một URL YouTube hợp lệ (ví dụ: `https://www.youtube.com/watch?v=jfKfPfyJRdk` - Lofi hip hop).
   - Bấm nút **"Nghe thử"**:
     - Nhãn trạng thái hiển thị: "Đang kết nối luồng nhạc..."
     - Sau 1-2 giây, âm thanh phát thử và nhãn trạng thái chuyển sang: "Đang phát thử nghiệm".
     - Bấm lại nút "Nghe thử" để dừng nghe thử.
   - Nhập một link sai (ví dụ `https://youtube.com/invalid_abcxyz`):
     - Bấm "Nghe thử" -> Nhãn trạng thái báo lỗi màu đỏ thân thiện: "Không tìm thấy video hoặc link không hợp lệ".
   - Dán lại link hợp lệ, bấm **"Lưu"**.
4. **Kiểm tra phát nhạc đồng bộ Slideshow**:
   - Slideshow đang phát ảnh: Nhạc nền phát êm dịu theo âm lượng đã chọn.
   - Bấm `Space` để tạm dừng trình chiếu: Nhạc nền lập tức tạm dừng.
   - Bấm `Space` để tiếp tục: Nhạc nền tiếp tục phát.
   - Bấm nút 🎵 trên thanh điều khiển: Tắt tiếng (icon chuyển thành 🔇); bấm lại để mở tiếng (icon chuyển thành 🎵).

---

## 2. Kịch Bản Kiểm Thử Xoay & Lật Ảnh (Transform Verification)

1. Mở một bức ảnh bất kỳ.
2. **Xoay phải 90°**:
   - Nhấn nút Xoay phải trên thanh điều khiển (hoặc phím tắt `R`).
   - **Kỳ vọng**: Ảnh xoay thuận chiều kim đồng hồ 90°, tự động căn chỉnh vừa vặn khung nhìn và không vượt quá mép màn hình.
3. **Lật ngang & lật dọc**:
   - Nhấn phím tắt `F` (Lật ngang) -> Ảnh lật đối xứng gương qua trục đứng.
   - Nhấn phím tắt `V` (Lật dọc) -> Ảnh lật đối xứng qua trục ngang.
4. **Kiểm tra bộ nhớ đệm phiên (Session Cache)**:
   - Đang ở bức ảnh đã xoay 90° và lật ngang, bấm phím mũi tên Phải (`Right Arrow`) để sang ảnh khác.
   - Bấm phím mũi tên Trái (`Left Arrow`) để quay lại ảnh cũ.
   - **Kỳ vọng**: Bức ảnh cũ hiển thị đúng góc xoay 90° và lật ngang như đã chỉnh trước đó.
5. **Kiểm tra tính an toàn dữ liệu**:
   - Kiểm tra tệp ảnh gốc trong thư mục ổ cứng -> Tệp tin hoàn toàn giữ nguyên ngày sửa đổi và kích thước pixel, không bị ghi đè.

---

## 3. Kịch Bản Kiểm Thử 5 Hiệu Ứng Chuyển Cảnh (Transitions Verification)

1. Mở Cài đặt (`⚙`), tìm mục "Hiệu ứng chuyển cảnh":
   - Danh sách hiển thị đủ 5 tùy chọn:
     - 1. Hòa tan / Mờ dần (Cross-Fade)
     - 2. Trượt sang trái (Slide Left)
     - 3. Trượt sang phải (Slide Right)
     - 4. Phóng to hòa trộn (Zoom Fade)
     - 5. Chuyển tức thì (Instant Cut)
2. Chọn **"Trượt sang trái (Slide Left)"**, bấm Lưu:
   - Bấm phím mũi tên Phải (`Next`): Ảnh mới trượt mượt mà từ phải sang trái.
   - Bấm phím mũi tên Trái (`Prev`): Hiệu ứng tự động đảo chiều, ảnh mới trượt từ trái sang phải như lật trang sách lùi.
3. Chọn **"Phóng to hòa trộn (Zoom Fade)"**, bấm Lưu:
   - Chuyển ảnh: Ảnh mới phóng to nhẹ nhàng kết hợp hòa tan mờ dần tạo chiều sâu thị giác.
4. Chọn **"Chuyển tức thì (Instant Cut)"**, bấm Lưu:
   - Chuyển ảnh: Ảnh đổi lập tức không trễ, phản hồi tức thời.

