# Research: Tinh Chỉnh Vòng Đời BGM Trong Cài Đặt & Khởi Tạo Âm Lượng

**Feature**: `008-fix-bgm-settings-and-volume`  
**Status**: Completed

## 1. Phân Tích & Giải Pháp Cho Vấn Đề 1 (Tắt Cài Đặt Làm Dừng Nhạc Nền)

### Hiện Trạng Codebase
Trong `src/presentation/views/settings_dialog.py`:
```python
def reject(self):
    self.stop_test_audio()
    super().reject()

def stop_test_audio(self):
    self.is_testing_audio = False
    self.btn_test_bgm.setText("▶ Nghe Thử")
    if self.presenter and self.presenter.manage_bgm_uc:
        self.presenter.manage_bgm_uc.stop()
```
Khi người dùng mở Cài đặt để xem thông số mà không hề bấm "Nghe thử" (`self.is_testing_audio == False`), khi họ nhấn nút "Hủy", phím `Esc` hoặc bấm dấu X, phương thức `reject()` vẫn gọi `stop_test_audio()`, dẫn đến việc gọi thẳng `self.presenter.manage_bgm_uc.stop()`, tắt luôn nhạc nền đang phát của màn hình chính!

### Quyết Định
- Trong `stop_test_audio()`: Chỉ gọi `self.presenter.manage_bgm_uc.stop()` KHI `self.is_testing_audio` đang là `True`:
  ```python
  def stop_test_audio(self):
      if not self.is_testing_audio:
          return
      self.is_testing_audio = False
      self.btn_test_bgm.setText("▶ Nghe Thử")
      if self.presenter and self.presenter.manage_bgm_uc:
          self.presenter.manage_bgm_uc.stop()
  ```
- Nhờ vậy, nếu người dùng không nghe thử trong Cài đặt, việc đóng/hủy hộp thoại hoàn toàn không ảnh hưởng đến bài nhạc đang phát ngoài màn hình chính.

---

## 2. Phân Tích & Giải Pháp Cho Vấn Đề 2 (Lưu Cài Đặt Dừng Nhạc Dù Không Đổi Link)

### Hiện Trạng Codebase
Trong `src/presentation/views/settings_dialog.py`:
1. `save_data()` luôn gọi `self.stop_test_audio()` và gọi `self.presenter.update_bgm_config(...)`.
2. Trong `ManageBgmUseCase.update_bgm_config(config)` (`src/application/use_cases.py`):
   ```python
   if config.enabled and config.youtube_url:
       self.music_player.set_source(config.youtube_url)
   else:
       self.music_player.stop()
   ```
   Bất cứ khi nào gọi `update_bgm_config`, kể cả khi người dùng chỉ chỉnh thời gian slideshow từ 3s sang 5s và bấm "Lưu", hàm này lại gọi `self.music_player.set_source(config.youtube_url)`, khiến luồng phát bị ngắt và tải lại từ đầu!

### Quyết Định
1. Trong `SettingsDialog.__init__`, lưu lại giá trị nguồn nhạc ban đầu khi vừa mở dialog:
   ```python
   self.initial_youtube_url = self.settings.bgm_youtube_url.strip()
   self.initial_bgm_source = self.settings.bgm_source
   ```
2. Trong `save_data()`:
   - Nếu `self.is_testing_audio`: dừng nghe thử bằng `stop_test_audio()`.
   - Lấy URL mới: `new_url = self.txt_youtube_url.text().strip()`.
   - Lấy nguồn mới: `new_source = self.cmb_bgm_source.currentData() or "youtube"`.
   - So sánh nguồn nhạc có thực sự thay đổi không:
     `url_changed = (new_url != self.initial_youtube_url) or (new_source != self.initial_bgm_source)`.
   - Nếu `url_changed`:
     - Nếu đang phát hoặc đang có nguồn, gọi dừng và nạp nguồn mới nếu có link.
   - Nếu `url_changed` là `False`:
     - KHÔNG gọi `set_source()`.
     - Chỉ cập nhật âm lượng (`set_volume`) và chế độ lặp (`set_loop`) mà không ngắt bài hát đang phát.

---

## 3. Phân Tích & Giải Pháp Cho Vấn Đề 3 (Mở App Lên Bấm Phát Nhạc Không Theo Âm Lượng Đã Lưu)

### Hiện Trạng Codebase
1. Trong `src/infrastructure/bgm/qt_music_player.py`:
   `self._volume: int = 70` (gán cứng 70).
2. Trong `main.py`:
   `music_player` được khởi tạo, sau đó `settings_repo.load_settings()` nạp cấu hình (chứa `settings.bgm_volume`), nhưng KHÔNG HỀ có dòng code nào đồng bộ `settings.bgm_volume` vào `music_player`!
3. Khi người dùng mở app lên và nhấn nút "🎵 Bật nhạc", `ManageBgmUseCase.play()` chỉ nạp nguồn và play, không cập nhật âm lượng của player theo config. Do đó player chạy với âm lượng mặc định 70% thay vì giá trị người dùng đã lưu (ví dụ 20%).

### Quyết Định
1. Trong `main.py`:
   Ngay sau khi khởi tạo `music_player` và `settings = settings_repo.load_settings()`, gọi:
   ```python
   music_player.set_volume(settings.bgm_volume)
   ```
2. Trong `ManageBgmUseCase.play()` (`src/application/use_cases.py`):
   Trước khi kích hoạt nạp hoặc phát nhạc, luôn đảm bảo âm lượng của player được đồng bộ chính xác:
   ```python
   self.music_player.set_volume(config.volume)
   ```
3. Đảm bảo trong `PhotoViewerWindow.init_ui()` hoặc `update_bgm_button_state()` trên thanh điều khiển option, thanh slider âm lượng hiển thị đúng giá trị `settings.bgm_volume`.

