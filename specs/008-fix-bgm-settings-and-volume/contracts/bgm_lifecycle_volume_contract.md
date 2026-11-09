# Interface Contracts: Tinh Chỉnh Vòng Đời BGM & Khởi Tạo Âm Lượng

**Feature**: `008-fix-bgm-settings-and-volume`  
**Status**: Ready

## 1. Application Layer Contract (`src/application/use_cases.py`)

### 1.1 `ManageBgmUseCase.apply_settings_without_reload(config: BgmConfig) -> None`
- **Mục đích**: Cập nhật các thông số âm lượng (`volume`) và lặp lại (`loop`) từ hộp thoại cài đặt mà KHÔNG làm gián đoạn bài hát đang phát.
- **Tham số**: `config: BgmConfig`
- **Hành vi**:
  1. Lưu cấu hình vào repository thông qua `self.settings_repo.save_settings(settings)`.
  2. Gọi `self.music_player.set_volume(config.volume)`.
  3. Gọi `self.music_player.set_loop(config.loop)`.
  4. TUYỆT ĐỐI KHÔNG gọi `self.music_player.set_source()`.

### 1.2 `ManageBgmUseCase.play() -> None`
- **Mục đích**: Bắt đầu phát nhạc từ màn hình chính.
- **Hành vi bổ sung**:
  - Luôn đảm bảo đồng bộ âm lượng `self.music_player.set_volume(config.volume)` trước khi kích hoạt `set_source()` hoặc `play()`.

---

## 2. Presentation Layer Contract (`src/presentation/views/settings_dialog.py`)

### 2.1 `stop_test_audio() -> None`
- **Điều kiện thực thi**:
  - Nếu `self.is_testing_audio == False`: Lập tức `return`, không gọi `manage_bgm_uc.stop()`.
  - Nếu `self.is_testing_audio == True`: Đặt `self.is_testing_audio = False`, đổi nhãn nút thành `"▶ Nghe Thử"` và gọi `self.presenter.manage_bgm_uc.stop()`.

### 2.2 `save_data() -> None`
- **Hành vi xác định thay đổi**:
  - So sánh `url_str` với `self.initial_youtube_url`.
  - So sánh nguồn với `self.initial_bgm_source`.
  - Nếu có thay đổi: Áp dụng cấu hình và dừng/nạp lại nguồn phát.
  - Nếu không đổi: Sử dụng `apply_settings_without_reload` hoặc chỉ cập nhật volume/loop, duy trì phát liên tục.

---

## 3. Composition Root Contract (`main.py`)
- **Hành vi**:
  - Sau khi `music_player` và `settings = settings_repo.load_settings()` được khởi tạo, gọi ngay lập tức:
    `music_player.set_volume(settings.bgm_volume)`

