# Data Model: Khắc Phục Luồng Bật Nhạc BGM Trên Thanh Option

**Feature**: `007-fix-bgm-play-button-flow`
**Status**: Ready

## 1. Overview
Tính năng này tinh chỉnh luồng kiểm tra trạng thái và kích hoạt phát nhạc BGM, không tạo thêm bảng cơ sở dữ liệu hay thực thể mới. Tuy nhiên, nó tái định nghĩa các ràng buộc về tính sẵn sàng và trạng thái phát nhạc giữa `ViewerSettings`, `BgmConfig`, `BgmPlaybackState`, và `MusicPlayerPort`.

---

## 2. Entities & Models

### 2.1 ViewerSettings (src/domain/models.py)
Cấu trúc cài đặt ứng dụng:
- `bgm_youtube_url: str`
  - URL nhạc YouTube hoặc luồng âm thanh được cấu hình.
  - Chuỗi rỗng `""` hoặc chỉ chứa khoảng trắng: Chưa có nhạc.
  - Chuỗi không rỗng hợp lệ (ví dụ `https://...`): Đã sẵn sàng phát.
- `bgm_volume: int`
  - Mức âm lượng từ `0` đến `100`.
- `bgm_enabled: bool` (Legacy Flag)
  - Được giữ lại để tương thích ngược cấu hình `settings.json`.
  - Quy tắc mới: Luôn đồng bộ `bgm_enabled = bool(bgm_youtube_url.strip())` khi nạp hoặc lưu.
  - Ràng buộc: Không còn được dùng làm điều kiện tiên quyết duy nhất để chặn phát nhạc.

### 2.2 BgmConfig (src/domain/models.py)
Đối tượng cấu hình BGM truyền giữa Presentation, Application và Infrastructure:
- `enabled: bool`: Thể hiện trạng thái cấu hình BGM có URL hợp lệ hay không (`bool(youtube_url.strip())`).
- `youtube_url: str`: URL nguồn phát.
- `volume: int`: Âm lượng (0-100).

### 2.3 BgmPlaybackState (src/domain/models.py)
Enum trạng thái phát nhạc:
- `STOPPED`: Nhạc đang dừng hoặc chưa nạp.
- `LOADING`: Đang phân giải stream hoặc tải dữ liệu audio.
- `PLAYING`: Đang phát nhạc.
- `PAUSED`: Tạm dừng.
- `ERROR`: Lỗi phân giải hoặc lỗi phát.

---

## 3. Trạng Thái & Chuyển Đổi Vòng Đời BGM (Lifecycle State Transitions)

```
[Khởi động App]
       │
       ▼
[STOPPED, current_target=""]
       │
       │ Người dùng nhấn "🎵 Bật nhạc"
       ▼
[ManageBgmUseCase.play()]
       │
       ├─ URL rỗng? ───────► Mở SettingsDialog
       │
       └─ URL hợp lệ & (current_target != url)
              │
              ▼
       [music_player.set_source(url)]
              │
              ▼
       [Trạng thái: LOADING ("⏳ Đang tải...")]
              │
              ├─ Lỗi trích xuất/mạng ──► [ERROR ("⚠️ Lỗi BGM") -> STOPPED ("🎵 Bật nhạc")]
              │
              └─ Nạp thành công ───────► [PLAYING ("⏸ Tắt nhạc")]
```

---

## 4. Ràng Buộc Dữ Liệu & Quy Tắc Nghiệp Vụ
1. **Tính sẵn sàng của BGM (`is_bgm_ready`)**:
   - Biểu thức điều kiện: `bool(bgm_youtube_url and bgm_youtube_url.strip())`.
   - Kết quả `True`: Nút BGM kích hoạt phát/dừng nhạc, không mở Cài đặt.
   - Kết quả `False`: Nút BGM mở Cài đặt để người dùng nhập link.

2. **Khởi tạo nguồn phát tự động (`auto_source_init`)**:
   - Khi người dùng bấm Play, nếu `player.current_target != config.youtube_url.strip()`, hệ thống bắt buộc gọi `music_player.set_source(url)`.
   - Khi đó, player tự động chuyển trạng thái `LOADING`, thực thi phân giải stream ngầm và bắt đầu phát nhạc ngay khi sẵn sàng.

