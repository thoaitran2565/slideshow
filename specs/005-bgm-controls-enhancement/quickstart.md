# Quickstart: Hướng Dẫn Kiểm Thử Xác Thực Nâng Cấp Điều Khiển Nhạc Nền

**Feature**: `005-bgm-controls-enhancement`
**Status**: Completed

Tài liệu này hướng dẫn kiểm thử xác thực 4 kịch bản cải tiến điều khiển âm thanh và giao diện.

---

## Kịch Bản 1: Cập Nhật Âm Lượng Trực Tiếp Khi "Nghe Thử" Trong Cài Đặt

1. Khởi chạy ứng dụng:
   ```powershell
   python main.py
   ```
2. Nhấp vào nút bánh răng "⚙️ Cài đặt" trên thanh điều khiển hoặc phím tắt để mở `SettingsDialog`.
3. Chuyển sang tab **"Nhạc Nền"**.
4. Nhập hoặc kiểm tra đường dẫn YouTube hợp lệ, sau đó bấm nút **"▶ Nghe Thử"**.
5. Trong khi âm thanh đang phát:
   - Kéo thanh trượt âm lượng từ mức hiện tại xuống `20%`.
   - **Xác nhận**: Độ lớn âm thanh loa phát ra giảm ngay lập tức theo cử chỉ chuột, không cần bấm dừng và nghe thử lại.
   - Kéo thanh trượt lên `80%`.
   - **Xác nhận**: Âm thanh to lên tức thời.

---

## Kịch Bản 2: Popup Chỉnh Âm Lượng Nhanh Bằng Chuột Phải

1. Mở màn hình xem ảnh với thanh điều khiển nổi (`ControlPanel`).
2. Di chuột đến nút BGM và **nhấp chuột phải** (Right-Click).
3. **Xác nhận**:
   - Một popup thanh trượt âm lượng nhỏ gọn xuất hiện ngay phía trên nút BGM với viền điểm nhấn Cyan hiện đại.
   - Hiển thị chính xác mức âm lượng % hiện hành.
4. Kéo thanh trượt âm lượng:
   - Nếu nhạc đang phát: Âm thanh thay đổi ngay lập tức theo thời gian thực.
5. Nhấp chuột ra ngoài vùng popup (ví dụ nhấp vào ảnh):
   - **Xác nhận**: Popup tự động đóng mượt mà, mức âm lượng mới được lưu lại.

---

## Kịch Bản 3: Kiểm Tra Nhãn Trực Quan "Bật Nhạc" / "Tắt Nhạc"

1. Khi nhạc nền đang tắt:
   - **Xác nhận**: Nút BGM hiển thị rõ ràng dòng chữ: `"🎵 Bật nhạc"`.
   - Rê chuột vào nút, tooltip hiển thị `"Bật nhạc nền (Chuột phải để chỉnh âm lượng)"`.
2. Bấm chuột trái vào nút để bật nhạc:
   - **Xác nhận**: Khi nhạc bắt đầu phát, nút tự động đổi nhãn thành `"🔇 Tắt nhạc"`.
   - Tooltip đổi thành `"Tắt nhạc nền (Chuột phải để chỉnh âm lượng)"`.
3. Bố cục thanh điều khiển không bị co vỡ chữ, căn giữa và hiển thị trọn vẹn.

---

## Kịch Bản 4: Khóa Chọn Các Nguồn Nhạc Chưa Khả Dụng

1. Mở hộp thoại `SettingsDialog`, chọn tab **"Nhạc Nền"**.
2. Nhấp chuột vào hộp chọn **"Nguồn phát nhạc"** (ComboBox).
3. **Xác nhận**:
   - Tùy chọn `"YouTube (Trực tuyến)"` có thể nhấp chọn bình thường.
   - Các tùy chọn `"Tệp ổ cứng cục bộ (Sắp ra mắt)"` và `"Spotify (Sắp ra mắt)"` bị làm mờ (disabled) và không thể nhấp chọn được.

