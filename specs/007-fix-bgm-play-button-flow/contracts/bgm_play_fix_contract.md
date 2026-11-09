# Interface & Behavioral Contracts: Khắc Phục Luồng Bật Nhạc BGM

**Feature**: `007-fix-bgm-play-button-flow`
**Status**: Ready

## 1. Presenter Interface Contract (`src/presentation/presenter.py`)

### 1.1 `is_bgm_ready() -> bool`
- **Mục đích**: Xác định xem ứng dụng đã có cấu hình nhạc nền sẵn sàng để phát hay chưa.
- **Tiền điều kiện**: `self.settings` đã được nạp từ repository.
- **Hành vi**:
  - Kiểm tra `self.settings.bgm_youtube_url`.
  - Trả về `True` nếu `bool(self.settings.bgm_youtube_url and self.settings.bgm_youtube_url.strip())` là `True`.
  - Trả về `False` nếu URL là `None`, chuỗi rỗng `""`, hoặc chỉ chứa ký tự khoảng trắng.
  - **TUYỆT ĐỐI KHÔNG** phụ thuộc vào giá trị boolean cũ của `self.settings.bgm_enabled`.

### 1.2 `play_bgm() -> None`
- **Mục đích**: Ủy nhiệm yêu cầu phát nhạc BGM xuống Use Case.
- **Hành vi**: Gọi `self.manage_bgm_use_case.play()`.

---

## 2. Application Use Case Contract (`src/application/use_cases.py`)

### 2.1 `ManageBgmUseCase.play() -> None`
- **Mục đích**: Điều phối phát nhạc nền BGM dựa trên cấu hình hiện hành.
- **Tiền điều kiện**: `self.music_player` (MusicPlayerPort) và `self.settings_repo` (SettingsRepositoryPort) đã được inject.
- **Hành vi**:
  1. Lấy cấu hình BGM hiện tại: `config = self.get_bgm_config()`.
  2. Lấy URL: `url = (config.youtube_url or "").strip()`.
  3. Nếu `url` là chuỗi rỗng: Không thực hiện phát nhạc (Presenter/View sẽ mở Settings nếu người dùng bấm nút).
  4. Nếu `url` hợp lệ:
     - Lấy target hiện tại của player: `player_target = getattr(self.music_player, "current_target", "")`.
     - Nếu `not player_target` HOẶC `player_target != url`:
       - Gọi `self.music_player.set_source(url)`.
     - Ngược lại (nếu player đã có sẵn source này và không cần nạp lại):
       - Gọi `self.music_player.play()`.

---

## 3. View Interaction Contract (`src/presentation/views/viewer_window.py`)

### 3.1 `toggle_bgm_action() -> None`
- **Mục đích**: Xử lý sự kiện khi người dùng click vào nút BGM trên thanh công cụ option.
- **Hành vi**:
  1. Kiểm tra trạng thái tải: Nếu BGM đang ở trạng thái `LOADING`, bỏ qua click.
  2. Kiểm tra tính sẵn sàng:
     - Gọi `if not self.presenter.is_bgm_ready():`
       - Mở `self.open_settings()` (focus tab Nhạc nền).
       - Kết thúc hàm.
  3. Nếu `is_bgm_ready()` là `True`:
     - Nếu đang phát (`PLAYING`): gọi `self.presenter.pause_bgm()`.
     - Nếu đang dừng hoặc tạm dừng (`STOPPED` / `PAUSED`): gọi `self.presenter.play_bgm()`.
     - Cập nhật hiển thị giao diện phù hợp.

