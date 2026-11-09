# Data Model: Tinh Chỉnh Vòng Đời BGM & Khởi Tạo Âm Lượng

**Feature**: `008-fix-bgm-settings-and-volume`  
**Status**: Ready

## 1. Entities & Fields

### 1.1 ViewerSettings (src/domain/models.py)
Các trường liên quan trực tiếp:
- `bgm_volume: int`
  - Miền giá trị: `[0, 100]`.
  - Mặc định: `70`.
  - Quy tắc: Được nạp từ `settings.json` khi khởi động ứng dụng và lập tức đồng bộ xuống `MusicPlayerPort`.
- `bgm_youtube_url: str`
  - URL hoặc Video ID của YouTube.
- `bgm_source: str`
  - Nguồn phát nhạc (mặc định `"youtube"`).
- `bgm_loop: bool`
  - Chế độ lặp lại bài hát.

### 1.2 SettingsDialog State (src/presentation/views/settings_dialog.py)
Các trạng thái phiên làm việc trong hộp thoại:
- `initial_youtube_url: str`: Chuỗi URL tại thời điểm mở dialog (đã qua `strip()`).
- `initial_bgm_source: str`: Nguồn phát tại thời điểm mở dialog.
- `is_testing_audio: bool`: Cờ chỉ định người dùng có đang nghe thử âm thanh bên trong dialog hay không.
  - `True`: Khi nhấn "▶ Nghe Thử" và đang phát thử.
  - `False`: Khi dừng nghe thử hoặc chưa từng bấm nghe thử.

---

## 2. State & Lifecycle Rules

### Quy Tắc 1: Đóng Hộp Thoại (Reject / Cancel / Esc / Close)
```
[Người dùng đóng SettingsDialog]
            │
            ▼
    is_testing_audio == True?
         /      \
      Có /        \ Không
        ▼          ▼
[Dừng nghe thử]  [KHÔNG tác động BGM ngoài màn hình chính]
```

### Quy Tắc 2: Lưu Cài Đặt (Save / Accept)
```
[Người dùng bấm Lưu]
            │
            ▼
(new_url != initial_url) HOẶC (new_source != initial_source)?
         /      \
      Có /        \ Không
        ▼          ▼
[Dừng bài cũ, nạp nguồn mới]  [Giữ nguyên bài đang phát, chỉ cập nhật volume/loop]
```

### Quy Tắc 3: Khởi Động Ứng Dụng (Application Boot)
```
[Khởi động main.py]
         │
         ▼
[load_settings() -> settings.bgm_volume]
         │
         ▼
[music_player.set_volume(settings.bgm_volume)]
         │
         ▼
[Sẵn sàng: Bấm Bật nhạc -> phát đúng âm lượng settings.bgm_volume]
```

