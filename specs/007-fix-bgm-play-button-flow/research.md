# Research: Khắc Phục Lỗi Nút Bật Nhạc BGM Trên Thanh Option

**Feature**: `007-fix-bgm-play-button-flow`
**Status**: Completed

## 1. Phân Tích Nguyên Nhân & Giải Pháp Cho Vấn Đề 1 (Nút BGM Mở Cài Đặt Dù Đã Có Link)

### Nguyên Nhân Gốc Rễ
Trong `src/presentation/presenter.py`, phương thức `is_bgm_ready()` được viết như sau:
```python
def is_bgm_ready(self) -> bool:
    return bool(self.settings.bgm_enabled and self.settings.bgm_youtube_url.strip())
```
Khi chúng ta loại bỏ ô checkbox "Kích hoạt nhạc nền khi trình chiếu" (`chk_bgm_enable`) ở Feature 006, cờ `bgm_enabled` trong tệp `settings.json` của người dùng có thể đang lưu giá trị `False` (do trước đó chưa từng tích checkbox hoặc cấu hình cũ). Khi người dùng bấm nút BGM trên màn hình chính:
```python
if not self.presenter.is_bgm_ready():
    self.open_settings()
```
Vì `bgm_enabled == False`, biểu thức `is_bgm_ready()` trả về `False`, khiến hệ thống luôn luôn kích hoạt mở hộp thoại `SettingsDialog` thay vì phát nhạc!

### Quyết Định
- Sửa đổi phương thức `is_bgm_ready()` để **chỉ kiểm tra sự tồn tại của chuỗi URL hợp lệ**:
  ```python
  def is_bgm_ready(self) -> bool:
      return bool(self.settings.bgm_youtube_url and self.settings.bgm_youtube_url.strip())
  ```
- Đồng thời, khi nạp hoặc lưu cấu hình, tự động chuẩn hóa `bgm_enabled = bool(self.settings.bgm_youtube_url.strip())`.

---

## 2. Phân Tích Nguyên Nhân & Giải Pháp Cho Vấn Đề 2 (Khởi Động App Bấm Phát Không Hoạt Động)

### Nguyên Nhân Gốc Rễ
Khi ứng dụng khởi động từ đầu:
1. `QtMusicPlayer` được khởi tạo với `self.current_target = ""` và chưa nạp bất kỳ nguồn phát nào.
2. Người dùng nhấp vào nút "🎵 Bật nhạc" ngoài màn hình chính:
   - `viewer_window.py` gọi `presenter.play_bgm()`.
   - `presenter.play_bgm()` gọi `ManageBgmUseCase.play()`.
3. Trong `ManageBgmUseCase.play()`:
   ```python
   def play(self) -> None:
       config = self.get_bgm_config()
       if config.enabled and config.youtube_url:
           self.music_player.play()
   ```
   - Thứ nhất: Nếu `config.enabled` là `False`, khối lệnh này hoàn toàn bị bỏ qua, không có bất kỳ hành động nào diễn ra!
   - Thứ hai: Kể cả nếu `config.enabled` là `True`, nó gọi trực tiếp `self.music_player.play()`.
4. Trong `QtMusicPlayer.play()`:
   ```python
   def play(self) -> None:
       if self.player.source().isEmpty() and self.current_target and self.provider:
           self.set_source(self.current_target)
           return
       self.player.play()
       self._set_playback_state(BgmPlaybackState.PLAYING)
   ```
   Vì `self.current_target` đang là `""` (chưa từng được gọi `set_source`), điều kiện `self.current_target` là `False`.
   Hàm chạy xuống gọi `self.player.play()` trên một `QMediaPlayer` rỗng không có media!
   Player không trích xuất stream, không chuyển sang `LOADING`, hoàn toàn im lặng!
5. Chỉ khi người dùng vào Cài đặt và bấm "Nghe thử", hàm `test_bgm_audio(url)` mới gọi `player.set_source(url)`, từ đó `self.current_target` mới được gán giá trị! Lúc này quay ra ngoài bấm nút BGM thì player mới có `current_target` để chạy!

### Quyết Định
- Nâng cấp `ManageBgmUseCase.play()`:
  ```python
  def play(self) -> None:
      config = self.get_bgm_config()
      url = config.youtube_url.strip()
      if url:
          player_target = getattr(self.music_player, "current_target", "")
          # Nếu player chưa có target hoặc target khác với url cấu hình thì nạp nguồn
          if not player_target or player_target != url:
              self.music_player.set_source(url)
          else:
              self.music_player.play()
  ```
- Nhờ cải tiến này, ngay khi vừa khởi động ứng dụng, người dùng bấm "🎵 Bật nhạc" là `ManageBgmUseCase` tự động nạp URL cấu hình vào `music_player.set_source(url)`, kích hoạt tức thì trạng thái `"⏳ Đang tải..."` và phát nhạc mượt mà không cần mồi trong Cài đặt!

