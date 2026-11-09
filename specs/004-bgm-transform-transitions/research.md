# Research & Technical Decisions: BGM, Transform & Transitions

**Feature**: `004-bgm-transform-transitions`  
**Date**: 2026-11-09  
**Status**: Completed  

---

## 1. Kiến Trúc Dịch Vụ Nhạc Nền (Background Music Service)

### Bối cảnh & Yêu cầu
- Cần hỗ trợ đa nguồn phát nhạc: YouTube (triển khai đầu tiên), Spotify (mở rộng sau), Tệp ổ cứng / MP3 (mở rộng sau).
- Phát âm thanh nền không làm đơ giao diện người dùng (Non-blocking I/O).
- Tích hợp điều khiển: Play/Pause theo slideshow, nút trên thanh Control Panel, nút "Nghe thử" và báo lỗi trong Settings.

### Các phương án đánh giá
| Tiêu chí | Phương án A: `yt-dlp` + `PyQt6.QtMultimedia` (Chọn) | Phương án B: `webbrowser` / Embedded WebView | Phương án C: Tải tệp MP3 về ổ cứng tạm (`tempfile`) |
|---|---|---|---|
| **Độ trễ & Hiệu năng** | Cao: Trích xuất direct audio stream URL (~1-2s), stream trực tiếp qua `QMediaPlayer`. | Kém: Nặng (Chromium engine ngốn 200MB+ RAM), khó giấu video UI. | Kém: Tải cả bài hát về đĩa gây trễ lớn (10-30s), tốn băng thông và dung lượng. |
| **Độ tự quản (Self-contained)** | Cao: `yt-dlp` và `PyQt6.QtMultimedia` có sẵn trong Python runtime, đóng gói PyInstaller dễ dàng. | Trung bình: Phụ thuộc `QtWebEngineCore` rất nặng (+150MB khi build). | Kém: Phụ thuộc ffmpeg tải về máy người dùng. |
| **Khả năng mở rộng** | Rất cao: Cổng `MusicPlayerPort` trừu tượng, mỗi provider (`YouTubeBgmProvider`, `LocalBgmProvider`, `SpotifyBgmProvider`) hiện thực độc lập. | Thấp: Bị bó buộc trong môi trường web iframe. | Trung bình. |

### Quyết định Kỹ thuật 1: `yt-dlp` Stream Extraction + `PyQt6.QtMultimedia.QMediaPlayer`
- **Quyết định**: Sử dụng `yt-dlp` với cấu hình trích xuất luồng âm thanh tốt nhất (`bestaudio/best`, `skip_download=True`) chạy trong luồng nền `QThread`. Khi có URL luồng, truyền cho `QMediaPlayer` phát qua `QAudioOutput`.
- **Xử lý nền (Non-blocking)**: Toàn bộ quá trình fetch URL YouTube được thực hiện trong `YouTubeStreamWorker(QThread)` để không gây gián đoạn giao diện trình chiếu ảnh 60 FPS.
- **Xử lý lỗi**: Bắt các ngoại lệ `DownloadError`, mất kết nối mạng hoặc video bị giới hạn địa lý; phát tín hiệu `error_occurred(str)` để hiển thị nhãn cảnh báo thân thiện trên giao diện.

---

## 2. Kiến Trúc Biến Đổi Hình Học Ảnh (Rotation & Flip)

### Bối cảnh & Yêu cầu
- Hỗ trợ xoay (90°, 180°, 270°) và lật ảnh (ngang, dọc).
- Bảo vệ dữ liệu gốc: Tuyệt đối không ghi đè tệp ảnh gốc trên đĩa.
- Duy trì bộ nhớ đệm trạng thái hiển thị trong phiên (`Session Transform Cache`).
- Tích hợp liền mạch với cơ chế `fitInView` và giới hạn thu nhỏ cơ sở $1.0x$ (Feature 003).

### Quyết định Kỹ thuật 2: Non-destructive `QTransform` on `QGraphicsPixmapItem`
- **Quyết định**: Áp dụng ma trận biến đổi `QTransform` xoay quanh tâm (`cx, cy = rect.width()/2, rect.height()/2`) và co dãn âm (`sx=-1` cho lật ngang, `sy=-1` cho lật dọc).
- **Đồng bộ khung nhìn**:
  ```python
  scene_bounds = item.mapToScene(item.boundingRect()).boundingRect()
  scene.setSceneRect(scene_bounds)
  view.fitInView(scene_bounds, Qt.AspectRatioMode.KeepAspectRatio)
  ```
- **Lưu trữ phiên**: `ViewerPresenter` duy trì từ điển `transform_cache: dict[str, ImageTransformState] = {}`. Khi đổi ảnh, presenter truy xuất trạng thái đã lưu để View áp dụng ngay lập tức. Khi tắt app, bộ nhớ đệm tự động giải phóng.

---

## 3. Kiến Trúc Bộ Điều Phối Hiệu Ứng Chuyển Cảnh (Transition Engine)

### Bối cảnh & Yêu cầu
- Cung cấp sẵn 5 hiệu ứng chuyển cảnh: *Fade, Slide Left, Slide Right, Zoom Fade, None*.
- Thiết kế dạng Pluggable Strategy Pattern để lập trình viên có thể bổ sung thêm nhiều hiệu ứng chuyển cảnh khác sau này mà không sửa đổi mã nguồn khung nhìn.
- Hỗ trợ tự động đảo chiều hiệu ứng trượt khi lùi ảnh (`Prev`).

### Quyết định Kỹ thuật 3: Pluggable Transition Strategy Pattern
- **Lớp cơ sở trừu tượng**:
  ```python
  class BaseTransition(QObject):
      def execute(self, view, current_item, next_pixmap, direction, duration_ms, on_finished):
          ...
  ```
- **5 Hiện thực ban đầu**:
  1. `CrossFadeTransition`: Sử dụng `QGraphicsOpacityEffect` chuyển dần độ mờ giữa 2 item.
  2. `SlideLeftTransition`: Di chuyển tọa độ X của ảnh mới từ cạnh phải sang trái; khi duyệt lùi (`Prev`) tự động đảo chiều từ trái sang phải.
  3. `SlideRightTransition`: Di chuyển tọa độ X của ảnh mới từ cạnh trái sang phải; khi duyệt lùi (`Prev`) tự động đảo chiều từ phải sang trái.
  4. `ZoomFadeTransition`: Kết hợp thay đổi tỷ lệ ma trận scale (1.1x -> 1.0x) và độ mờ opacity.
  5. `InstantTransition`: Hoán đổi pixmap lập tức với thời gian 0ms.
- **Quản lý chuyển cảnh an toàn**: Hủy an toàn animation cũ (`anim.stop()`) trước khi bắt đầu animation mới để ngăn xung đột khi người dùng bấm Next/Prev liên tục với tốc độ cao.

