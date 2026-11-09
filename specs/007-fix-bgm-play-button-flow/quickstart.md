# Quickstart & Verification Guide: Khắc Phục Luồng Bật Nhạc BGM

**Feature**: `007-fix-bgm-play-button-flow`
**Status**: Ready

## 1. Mục Đích Kiểm Thử
Xác nhận rằng:
1. Khi đã có link nhạc trong Cài đặt (kể cả khi `bgm_enabled: false` trong file `settings.json`), nhấn nút BGM ở màn hình chính sẽ phát nhạc (hoặc hiển thị Loading), **tuyệt đối không mở Cài đặt**.
2. Khi mở ứng dụng lần đầu và nhấn nút BGM, ứng dụng tự động nạp nguồn và phát nhạc ngay lập tức mà **không cần phải vào Cài đặt bấm "Nghe thử" trước**.
3. Khi chưa cài đặt link nhạc (URL rỗng), nhấn nút BGM sẽ mở hộp thoại Cài đặt (chuyển thẳng đến tab Nhạc nền).

---

## 2. Các Bước Kiểm Thử Thủ Công

### Kịch bản 1: Kiểm tra nút BGM khi đã có link (Vấn đề 1 & Vấn đề 2)
1. Đảm bảo trong `settings.json` có trường `bgm_youtube_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"` và `bgm_enabled: false` (giả lập cấu hình người dùng cũ).
2. Khởi động ứng dụng:
   ```powershell
   python main.py
   ```
3. Quan sát nút BGM trên thanh công cụ option dưới đáy màn hình (hiện "🎵 Bật nhạc").
4. **Nhấp chuột trái vào nút "🎵 Bật nhạc"**.
5. **Kỳ vọng**:
   - Hộp thoại Cài đặt **KHÔNG** bị bật lên.
   - Nút BGM lập tức chuyển sang trạng thái "⏳ Đang tải..." (loading).
   - Sau khi phân giải/nạp stream, nút BGM chuyển sang "⏸ Tắt nhạc" và âm thanh phát ra.

### Kịch bản 2: Kiểm tra khi chưa có link BGM
1. Mở Cài đặt, xóa sạch link nhạc BGM và bấm Lưu.
2. Đóng ứng dụng và mở lại.
3. Nhấp chuột trái vào nút "🎵 Bật nhạc".
4. **Kỳ vọng**:
   - Do chưa có link, ứng dụng tự động mở `SettingsDialog` và chuyển đến tab Nhạc nền để người dùng nhập link.

---

## 3. Kiểm Thử Tự Động (Automated Regression Test)
Chạy script kiểm thử PyQt tự động để đảm bảo logic không bị lỗi hồi quy:
```powershell
python tests/test_feature_007.py
```
Script kiểm thử bao gồm các bài test:
- Test 1: `is_bgm_ready()` trả về `True` khi có URL kể cả khi `bgm_enabled == False`.
- Test 2: `is_bgm_ready()` trả về `False` khi URL rỗng.
- Test 3: `ManageBgmUseCase.play()` tự động gọi `set_source(url)` khi `current_target` chưa được nạp.
- Test 4: `toggle_bgm_action()` kích hoạt `play_bgm()` chứ không mở `open_settings()`.

---

## 4. Kiểm Tra Đóng Gói PyInstaller
Sau khi kiểm thử thành công, chạy lệnh đóng gói:
```powershell
python -m PyInstaller -y slideshow.spec
```
Xác nhận tệp `dist/Slideshow.exe` chạy mượt mà, khởi động không lỗi.

