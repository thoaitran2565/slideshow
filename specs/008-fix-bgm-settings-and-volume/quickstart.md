# Quickstart & Verification Guide: Vòng Đời BGM & Âm Lượng

**Feature**: `008-fix-bgm-settings-and-volume`  
**Status**: Ready

## 1. Kịch Bản Kiểm Thử Thủ Công

### Kịch bản 1: Mở và Đóng/Hủy Cài Đặt Không Làm Tắt Nhạc Nền
1. Khởi động ứng dụng bằng `python main.py`.
2. Bấm nút "🎵 Bật nhạc" trên thanh công cụ option để nhạc bắt đầu phát.
3. Bấm vào nút bánh răng "⚙" để mở hộp thoại Cài đặt.
4. Không bấm nút "Nghe thử". Bấm nút "Hủy" (hoặc bấm dấu X góc trên, hoặc nhấn `Esc`).
5. **Kỳ vọng**: Nhạc nền ngoài màn hình chính vẫn tiếp tục phát mượt mà, không bị tắt đột ngột.

### Kịch bản 2: Bấm "Lưu" Cài Đặt Khi Không Đổi Link Nhạc
1. Nhạc nền đang phát.
2. Mở Cài đặt, đổi thời gian hiển thị ảnh từ 3s sang 5s (giữ nguyên link YouTube).
3. Bấm nút "Lưu".
4. **Kỳ vọng**: Hộp thoại đóng lại, thời gian slideshow cập nhật thành 5s, và bài hát đang phát tiếp tục phát bình thường, không bị dừng hay tải lại từ đầu.

### Kịch bản 3: Đổi Link Nhạc Mới Rồi Bấm "Lưu"
1. Nhạc nền đang phát.
2. Mở Cài đặt, nhập một link YouTube khác hoặc xóa trắng link và bấm "Lưu".
3. **Kỳ vọng**: Bài hát cũ dừng phát; nếu có link mới thì nạp bài mới.

### Kịch bản 4: Kiểm Tra Âm Lượng Khởi Động
1. Trong Cài đặt hoặc trên thanh công cụ option, kéo âm lượng về 25%. Đóng ứng dụng hoàn toàn.
2. Kiểm tra tệp `settings.json` xác nhận `"bgm_volume": 25`.
3. Mở lại ứng dụng bằng `python main.py`.
4. Bấm nút "🎵 Bật nhạc".
5. **Kỳ vọng**: Âm thanh phát ra ở đúng mức âm lượng nhỏ 25%, slider âm lượng trên thanh option hiển thị đúng 25%.

---

## 2. Kiểm Thử Tự Động
Chạy kịch bản kiểm thử:
```powershell
python tests/test_feature_008.py
```
Đảm bảo tất cả các bài kiểm tra đều vượt qua 100%.

---

## 3. Kiểm Tra Đóng Gói PyInstaller
```powershell
python -m PyInstaller -y slideshow.spec
```
Xác nhận tệp `dist/Slideshow.exe` biên dịch thành công và khởi động tốt.

