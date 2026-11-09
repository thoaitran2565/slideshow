# Research: Tinh Chỉnh Vòng Đời Nhạc Nền, Lớp Phủ Chống Click Xuyên & Tối Ưu Mượt Mà Zoom Fade

**Feature**: `006-bgm-lifecycle-and-zoom-polish`
**Status**: Completed

## 1. Tách Rời Vòng Đời BGM & Loại Bỏ Checkbox Cài Đặt

### Vấn Đề
Trước đây, hàm `toggle_play_pause()` của slideshow tự động đồng bộ gọi `play_bgm()` hoặc `pause_bgm()`. Điều này gây bất tiện khi người dùng muốn dừng slideshow để ngắm một bức ảnh đẹp nhưng vẫn muốn nghe nhạc nền tiếp tục phát. Ngoài ra, việc tồn tại checkbox "Kích hoạt nhạc nền khi trình chiếu" trong Cài đặt là thừa thãi vì người dùng đã có nút BGM dứt khoát trên thanh công cụ.

### Quyết Định
- Tách rời hoàn toàn: `toggle_play_pause()` chỉ kiểm soát timer chuyển slide của slideshow. Không gọi hàm liên quan đến BGM.
- Loại bỏ `chk_bgm_enable` trong `SettingsDialog`. Quyền bật/tắt BGM thuộc về nút bấm trên thanh công cụ `ControlPanel`.
- Tự động ngắt BGM khi sửa link hoặc bấm nghe thử trong Cài đặt: Khi phát hiện tín hiệu `textEdited` trên ô nhập URL hoặc khi bấm nút "▶ Nghe Thử", nếu presenter đang phát nhạc nền ngoài màn hình chính thì lập tức gọi `presenter.stop_bgm()` để tránh xung đột âm thanh.

---

## 2. Quản Lý Trạng Thái Loading Nạp Nhạc & Safety Timeout (15 Giây)

### Vấn Đề
Khi người dùng bấm "Bật nhạc", việc trích xuất stream từ YouTube qua `yt-dlp` cần từ 1 đến 3 giây (hoặc lâu hơn nếu mạng chậm). Nếu không có phản hồi trực quan, người dùng tưởng nút bị đơ và bấm liên tục, gây spam luồng nạp stream. Hơn nữa nếu mạng bị đứt, tiến trình có thể treo vĩnh viễn ở trạng thái chờ.

### Quyết Định
- Định nghĩa mô hình trạng thái: `BgmPlaybackState`: `STOPPED`, `LOADING`, `PLAYING`, `ERROR`.
- Khi người dùng bấm "Bật nhạc":
  - Nút BGM đổi text thành `"⏳ Đang tải..."`, bị vô hiệu hóa `setEnabled(False)`.
  - Tab Nhạc Nền trong Cài đặt hiển thị nhãn `"⏳ Đang kết nối luồng nhạc..."` và tạm khóa nút nghe thử và ô nhập URL.
  - Kích hoạt một `QTimer` one-shot 15.000 ms (15 giây) an toàn.
  - Nếu quá 15 giây mà luồng nhạc chưa phát được: timer kích hoạt -> hủy tiến trình trích xuất -> chuyển sang `ERROR` -> phát thông báo tooltip đỏ `"Lỗi: Quá thời gian nạp nhạc (Timeout 15s)"` -> phục hồi nút BGM về `"🎵 Bật nhạc"` và mở khóa lại tương tác (Option A).
  - Nếu phát thành công trước 15s: hủy timer timeout -> chuyển sang `PLAYING` -> nút BGM chuyển thành `"🔇 Tắt nhạc"` và mở khóa tương tác.

---

## 3. Lớp Phủ Trong Suốt Chống Click Xuyên (Transparent Modal Backdrop Overlay)

### Vấn Đề
Khi mở Quick Volume Popup bằng chuột phải, người dùng muốn nhấp chuột ra ngoài để đóng popup. Tuy nhiên nếu nhấp chuột vào các nút khác (Pause, Random, Next) hoặc vào canvas ảnh thì cú nhấp chuột đó có thể vô tình kích hoạt sự kiện click của các nút bên dưới.

### Quyết Định
- Tạo lớp `BackdropOverlay(QWidget)` gắn vào cửa sổ chính `PhotoViewerWindow`.
- Overlay có kích thước phủ kín cửa sổ (`setGeometry(self.rect())`) với nền trong suốt không màu (`background-color: transparent;`).
- Ghi đè `mousePressEvent(event)` trên `BackdropOverlay`: Khi có sự kiện click chuột rơi vào overlay, overlay sẽ gọi đóng `QuickVolumePopup`, ẩn chính mình và gọi `event.accept()`. Nhờ cơ chế chặn sự kiện của Qt, cú click chuột này bị tiêu thụ hoàn toàn, không xuyên thấu xuống các widget bên dưới.

---

## 4. Tối Ưu Hóa Mượt Mà Hiệu Ứng Zoom Fade (Smooth Zoom Fade)

### Vấn Đề
Trong `ZoomFadeTransition`, ảnh mới `next_pixmap` được gán trực tiếp vào `incoming_item` với kích thước pixel gốc (ví dụ 4K hoặc 800x600). Khi áp dụng scale quanh tâm, ảnh mới xuất hiện to đùng hoặc nhỏ xíu không khớp với khung nhìn viewport, sau khi animation kết thúc mới gọi `fit_image_in_view()`, gây ra cú giật nảy khung hình khó chịu.

### Quyết Định
- Tính toán kích thước mục tiêu khớp với khung nhìn (`viewport_size = view.viewport().size()`).
- Tính toán tỉ lệ chuẩn hóa $S_{base} = \min(vw / pw, vh / ph)$ sao cho ảnh mới vừa khít khung nhìn tương tự `fitInView` ngay từ frame đầu tiên.
- Thiết lập tâm biến đổi đồng tâm với khung nhìn hiển thị:
  - Căn giữa ảnh mới tại vị trí chuẩn xác trong scene.
  - Hoạt ảnh biến đổi:
    - Ảnh cũ: Phóng nhẹ từ $1.0x$ lên $1.06x$, opacity từ $1.0 \rightarrow 0.0$.
    - Ảnh mới: Thu phóng nhẹ từ $0.94x \rightarrow 1.0x$, opacity từ $0.0 \rightarrow 1.0$.
- Nhờ việc ảnh mới đã ở đúng tỉ lệ và vị trí vừa vặn từ frame $0$, khi hoạt ảnh kết thúc và chuyển sang `current_item`, kích thước và vị trí hoàn toàn trùng khớp 100%, đem lại chuyển động hòa tan siêu mượt mà ở 60 FPS.

