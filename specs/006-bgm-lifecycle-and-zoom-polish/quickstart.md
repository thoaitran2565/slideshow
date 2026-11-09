# Quickstart: Hướng Dẫn Kiểm Thử Tinh Chỉnh Vòng Đời BGM & Mượt Mà Zoom Fade

**Feature**: `006-bgm-lifecycle-and-zoom-polish`
**Status**: Completed

Tài liệu này hướng dẫn kiểm thử xác thực 4 kịch bản cải tiến vòng đời BGM, lớp phủ và Zoom Fade.

---

## Kịch Bản 1: Độc Lập Vòng Đời Nhạc Nền Với Slideshow

1. Khởi chạy ứng dụng: `python main.py`.
2. Bấm nút **"🎵 Bật nhạc"** trên thanh điều khiển.
3. Chờ nhạc bắt đầu phát.
4. Bấm **Phím cách (Space)** hoặc nút **"⏸ Pause"** trên thanh điều khiển để tạm dừng trình chiếu.
5. **Xác nhận**: Ảnh ngừng chuyển nhưng âm thanh nhạc nền vẫn tiếp tục phát liền mạch không ngắt quãng.
6. Bấm Space tiếp tục trình chiếu; slide chạy tiếp và nhạc vẫn phát bình thường.

---

## Kịch Bản 2: Trạng Thái Loading Nạp Nhạc & Safety Timeout

1. Bấm nút **"🎵 Bật nhạc"**.
2. **Xác nhận**:
   - Ngay tức thì, nút BGM đổi nhãn sang `"⏳ Đang tải..."` và bị vô hiệu hóa click (không thể bấm liên tục).
3. Trong lúc đang tải, mở **"⚙️ Cài đặt"**, chọn tab **"Nhạc Nền"**:
   - **Xác nhận**: Hiển thị trạng thái `"⏳ Đang kết nối luồng nhạc..."`, ô nhập URL và nút nghe thử tạm khóa.
4. Trường hợp link hỏng hoặc thử nghiệm ngắt mạng:
   - **Xác nhận**: Đúng 15 giây sau, hệ thống dừng tiến trình, hiển thị tooltip thông báo lỗi màu đỏ, nút phục hồi về nhãn `"🎵 Bật nhạc"` và mở khóa tương tác bình thường.

---

## Kịch Bản 3: Lớp Phủ Chống Click Xuyên Khi Đóng Popup Âm Lượng

1. Nhấp chuột phải vào nút BGM để mở **Quick Volume Popup**.
2. Rê chuột ra ngoài phạm vi thanh âm lượng và nhấp vào nút **"⏸ Pause"** hoặc nhấp vào vùng ảnh.
3. **Xác nhận**:
   - Popup âm lượng biến mất ngay lập tức.
   - Nút "Pause" KHÔNG bị bấm (slideshow không bị đổi trạng thái), và ảnh KHÔNG bị click phóng to hay chuyển ảnh.

---

## Kịch Bản 4: Mượt Mà Tuyệt Đối Hiệu Ứng Zoom Fade

1. Mở Cài đặt, chọn hiệu ứng chuyển cảnh là **"Phóng to hòa trộn (Zoom Fade)"** và bấm Lưu.
2. Mở một thư mục ảnh có các ảnh độ phân giải chênh lệch lớn (ví dụ ảnh dọc nhỏ xen lẫn ảnh phong cảnh ngang 4K).
3. Bấm Next chuyển slide liên tục.
4. **Xác nhận**:
   - Hai bức ảnh hòa quyện mượt mà ở 60 FPS, tỷ lệ co giãn đồng tâm chuẩn xác, không còn hiện tượng giật nảy hay phóng to quá cỡ trước khi co lại.

