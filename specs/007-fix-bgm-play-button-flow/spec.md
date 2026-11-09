# Feature Specification: Khắc Phục Lỗi Nút Bật Nhạc BGM Trên Thanh Option

**Feature Branch**: `007-fix-bgm-play-button-flow`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "sửa lỗi khi bấm nút bật nhạc dưới thanh option, nó có 2 vẫn đề là khi trong cài đặt đã setup nhạc rồi mà bấm vô nó vẫn mở cài đặt lên mà không phát nhạc, vấn đề 2 khi đôi khi mở app lên bấm phát nhạc thì nó không hoạt động cũng không thay đổi trạng thái hay loading gì chỉ khi mở cài đặt lên và bấm nghe thử thì lúc này nút bấm này mới hoạt động khi bấm"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Kích Hoạt Phát Nhạc Ngay Khi Đã Có Cấu Hình Link YouTube (Priority: P1) 🎯 MVP

Là một người dùng đã cấu hình đường dẫn YouTube trong Cài đặt, khi tôi bấm vào nút "🎵 Bật nhạc" trên thanh công cụ điều khiển ở màn hình chính, tôi muốn ứng dụng lập tức phát nhạc nền (hoặc chuyển sang trạng thái nạp nhạc) mà KHÔNG tự động mở hộp thoại Cài đặt lên.

**Why this priority**: Khắc phục lỗi điều hướng sai logic nghiêm trọng khiến người dùng không thể bật nhạc trực tiếp từ giao diện xem ảnh chính.

**Independent Test**: Đảm bảo trong Cài đặt đã lưu một link YouTube hợp lệ; quay ra màn hình xem ảnh chính, nhấp chuột trái vào nút "🎵 Bật nhạc"; ứng dụng bắt đầu phát nhạc ngay lập tức (nút chuyển sang Loading rồi phát), hộp thoại Cài đặt hoàn toàn không bị bật lên.

**Acceptance Scenarios**:

1. **Given** người dùng đã lưu link YouTube trong `settings.json`, **When** người dùng nhấp nút "🎵 Bật nhạc" trên thanh điều khiển, **Then** hệ thống nhận diện nhạc đã sẵn sàng (`is_bgm_ready() == True`), không mở `SettingsDialog` và bắt đầu kích hoạt phát nhạc.
2. **Given** người dùng chưa hề nhập link YouTube (chuỗi rỗng hoặc chỉ toàn khoảng trắng), **When** người dùng nhấp nút "🎵 Bật nhạc", **Then** hệ thống tự động mở `SettingsDialog` để người dùng thiết lập nguồn nhạc.

---

### User Story 2 - Tự Động Nạp Nguồn & Phát Nhạc Khi Khởi Động Ứng Dụng Mới (Priority: P1)

Là một người dùng vừa mở ứng dụng lên (phiên làm việc mới), tôi muốn có thể bấm nút "🎵 Bật nhạc" trên thanh công cụ để nghe nhạc ngay lập tức với đầy đủ trạng thái "⏳ Đang tải..." rồi phát âm thanh, KHÔNG cần phải mở hộp thoại Cài đặt và bấm nút "Nghe thử" thì nút ngoài mới chịu hoạt động.

**Why this priority**: Khắc phục lỗi vòng đời khởi tạo chưa truyền URL nguồn phát xuống `QtMusicPlayer`, đảm bảo tính khả dụng độc lập của nút BGM mọi lúc mọi nơi.

**Independent Test**: Tắt ứng dụng và mở lại từ đầu; không vào Cài đặt; nhấp ngay vào nút "🎵 Bật nhạc"; nút đổi sang `"⏳ Đang tải..."`, hệ thống tự động nạp nguồn YouTube đã lưu và phát ra loa sau 1-2 giây.

**Acceptance Scenarios**:

1. **Given** ứng dụng vừa khởi động và người dùng chưa từng mở Cài đặt trong phiên này, **When** người dùng bấm nút "🎵 Bật nhạc", **Then** hệ thống tự động nạp nguồn URL từ cấu hình xuống trình phát (`set_source`), kích hoạt trạng thái Loading và phát nhạc thành công.
2. **Given** trình phát nhạc đang ở trạng thái dừng hoặc chưa nạp luồng, **When** phương thức `play()` được gọi, **Then** hệ thống tự kiểm tra và nạp nguồn nếu trình phát chưa có nguồn, đảm bảo không bao giờ rơi vào trạng thái im lặng không phản hồi.

---

### Edge Cases

- **Tệp settings.json có cờ cũ `bgm_enabled = False` nhưng có URL**: Hệ thống tự động chuẩn hóa coi cờ này là `True` khi có URL hợp lệ, không chặn người dùng.
- **Người dùng gõ URL chứa khoảng trắng đầu/cuối**: Hệ thống tự động `strip()` và kiểm tra độ dài chuỗi trước khi xác định trạng thái sẵn sàng.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Hệ thống MUST xác định trạng thái sẵn sàng của nhạc nền (`is_bgm_ready()`) chỉ dựa trên sự tồn tại của chuỗi đường dẫn URL hợp lệ (`bool(bgm_youtube_url.strip())`), LOẠI BỎ hoàn toàn sự phụ thuộc vào cờ phụ `bgm_enabled` cũ.
- **FR-002**: Khi phương thức `ManageBgmUseCase.play()` được gọi, nếu trình phát nhạc (`music_player`) chưa được nạp nguồn hoặc nguồn hiện tại khác với URL trong cấu hình, hệ thống MUST tự động gọi `music_player.set_source(config.youtube_url)` để khởi tạo tiến trình nạp và phát nhạc.
- **FR-003**: Khi người dùng nhấn nút BGM ("🎵 Bật nhạc") trên thanh điều khiển nổi:
  - Nếu đã có URL: Bắt đầu phát hoặc chuyển sang trạng thái `"⏳ Đang tải..."` ngay lập tức, TUYỆT ĐỐI KHÔNG mở hộp thoại Cài đặt.
  - Nếu chưa có URL: Tự động mở hộp thoại Cài đặt (`SettingsDialog`) để người dùng cấu hình.
- **FR-004**: Khi ứng dụng khởi động hoặc lưu cấu hình mới, giá trị `bgm_enabled` MUST tự động đồng bộ giá trị với `bool(bgm_youtube_url.strip())` nhằm đảm bảo tương thích dữ liệu 100%.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% các lần bấm nút BGM khi đã có link YouTube trong cài đặt sẽ kích hoạt phát nhạc trực tiếp, tỷ lệ mở nhầm Cài đặt là 0%.
- **SC-002**: 100% các phiên khởi động mới của ứng dụng, nút BGM phản hồi ngay tức thì (< 30ms) với trạng thái loading và tự động nạp nguồn phát thành công mà không đòi hỏi bất kỳ thao tác mồi nào trong Cài đặt.

## Assumptions

- Đường dẫn YouTube đã lưu là một URL hoặc Video ID có thể truy cập được; nếu mạng lỗi thì Safety Timeout 15s đã cài đặt ở Feature 006 sẽ xử lý an toàn.

