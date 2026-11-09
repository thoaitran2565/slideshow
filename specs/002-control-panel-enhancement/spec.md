# Feature Specification: Nâng Cao Độ Rõ Nét & Ghi Nhớ Trạng Thái Thanh Điều Khiển

**Feature Branch**: `002-control-panel-enhancement`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "- Cập nhật ui thanh option bên dưới, nếu ảnh có màu sáng quá ở khu vực đó thì thanh option sẽ bị quá mờ và khó nhìn, hãy cho nó nhìn rõ hơn kể khi ảnh quá sáng\n- lưu lại trạng thái khi người dùng bấm random và ẩn hiện thanh option, khi tắt app mở lại nó vẫn ghi nhớ các lựa chọn này"

## Clarifications

### Session 2026-11-09
- Q: Để đảm bảo thanh điều khiển luôn nhìn rõ trên các bức ảnh có màu trắng hoặc nền quá sáng, chúng ta nên áp dụng kỹ thuật tách lớp thị giác nào? → A: Option A (Thẻ nổi Floating Card: Nền đen đặc `#121212` 95%, viền sáng tương phản và hiệu ứng đổ bóng nổi `QGraphicsDropShadowEffect` màu đen đậm với blur radius $\ge 24px$ bao quanh thanh điều khiển và nút "Hiện thanh công cụ").

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hiển Thị Rõ Nét Thanh Điều Khiển Trên Mọi Nền Ảnh Sáng (Priority: P1)

Là một người xem ảnh với nhiều bức ảnh có độ sáng cao (ảnh phong cảnh tuyết, tài liệu trắng, hình chụp ngoài trời nắng), tôi muốn thanh điều khiển (Control Panel) bên dưới và các nút bấm luôn hiển thị sắc nét, tương phản rõ ràng và không bị chìm hay mờ lóa, để tôi có thể dễ dàng nhận biết và tương tác với các nút bấm mà không bị mỏi mắt.

**Why this priority**: Trải nghiệm xem ảnh cốt lõi bị ảnh hưởng trực tiếp nếu người dùng không thể nhìn rõ nút bấm và trạng thái tốc độ khi gặp ảnh sáng màu.

**Independent Test**: Mở một bức ảnh có màu trắng hoàn toàn (`#FFFFFF`) hoặc độ sáng cực cao ở nửa dưới màn hình; xác nhận thanh điều khiển, các nút chức năng, chữ hiển thị "Tốc độ: 3s" và viền bao quanh vẫn hiển thị nổi bật, rõ ràng 100%.

**Acceptance Scenarios**:

1. **Given** ảnh đang hiển thị có khu vực đáy màu trắng hoặc độ sáng cao, **When** thanh điều khiển xuất hiện ở dưới màn hình, **Then** thanh điều khiển có nền đen đặc `#121212` (95%), viền sáng tương phản và hiệu ứng đổ bóng nổi `QGraphicsDropShadowEffect`, giúp toàn bộ nội dung chữ và nút bấm đọc được dễ dàng mà không bị hòa lẫn vào ảnh.
2. **Given** thanh công cụ bị ẩn khi đang xem ảnh nền trắng, **When** nút "👁️ Hiện thanh công cụ" hiển thị, **Then** nút này cũng áp dụng hiệu ứng đổ bóng `QGraphicsDropShadowEffect` và viền tương phản cao, nổi bật hoàn toàn trên nền ảnh trắng.

---

### User Story 2 - Ghi Nhớ Trạng Thái Chế Độ Phát Ngẫu Nhiên (Random Mode Persistence) (Priority: P1)

Là một người dùng ưa thích xem ảnh ngẫu nhiên, tôi muốn trạng thái bật/tắt của chế độ Random được tự động lưu lại, để khi tôi tắt ứng dụng và khởi động lại vào lần sau, ứng dụng vẫn tiếp tục phát ảnh ngẫu nhiên mà không bắt tôi phải bấm lại nút Random thủ công mỗi lần mở app.

**Why this priority**: Nâng cao tính tiện dụng cá nhân hóa, giảm thiểu thao tác lặp lại không cần thiết cho người dùng thường xuyên.

**Independent Test**: Bật nút "🔀 Random" (trạng thái checked), đóng ứng dụng, mở lại ứng dụng; xác nhận nút Random vẫn ở trạng thái checked và danh sách ảnh được phát theo thứ tự ngẫu nhiên.

**Acceptance Scenarios**:

1. **Given** ứng dụng đang chạy ở chế độ tuần tự, **When** người dùng nhấp bật nút "🔀 Random", **Then** trạng thái `is_random: true` được lưu ngay lập tức vào cấu hình `settings.json`.
2. **Given** người dùng đã bật Random ở phiên trước, **When** khởi động lại ứng dụng, **Then** giao diện hiển thị nhãn `🔀 Random - <tên file>` và nút Random trên thanh điều khiển được kích hoạt sẵn.

---

### User Story 3 - Ghi Nhớ Trạng Thái Ẩn/Hiện Thanh Điều Khiển (Visibility Persistence) (Priority: P2)

Là một người dùng thích xem ảnh tập trung tối đa không bị vướng bảng điều khiển, tôi muốn trạng thái ẩn thanh công cụ được ghi nhớ, để khi tôi mở app lên, giao diện giữ nguyên không gian xem ảnh thoáng đãng mà tôi đã thiết lập trước đó.

**Why this priority**: Tôn trọng sở thích bố cục giao diện của từng người dùng qua các phiên làm việc.

**Independent Test**: Bấm nút "Ẩn" hoặc phím tắt `H` để ẩn thanh công cụ, tắt ứng dụng, khởi động lại; xác nhận thanh công cụ vẫn ẩn và nút "Hiện thanh công cụ" hiển thị sẵn sàng.

**Acceptance Scenarios**:

1. **Given** thanh công cụ đang hiển thị, **When** người dùng bấm nút "👁️ Ẩn" hoặc phím tắt `H`, **Then** thanh công cụ ẩn đi, nút "👁️ Hiện thanh công cụ" xuất hiện và giá trị `show_control_panel: false` được lưu vào `settings.json`.
2. **Given** người dùng đã ẩn thanh công cụ ở phiên trước, **When** mở lại ứng dụng, **Then** thanh công cụ vẫn ẩn và nút "👁️ Hiện thanh công cụ" sẵn sàng cho phép người dùng mở lại khi cần.

---

### Edge Cases

- **Tệp cấu hình `settings.json` cũ chưa có các khóa mới (`is_random`, `show_control_panel`)**: Tầng nạp cấu hình phải áp dụng giá trị mặc định an toàn (`is_random = False`, `show_control_panel = True`) mà không gây lỗi.
- **Người dùng bấm phím tắt `H` liên tục**: Trạng thái hiển thị và lưu cấu hình phải được đồng bộ tức thời, không xảy ra xung đột vẽ khung hình.
- **Màn hình ở độ phân giải nhỏ hoặc resize cửa sổ**: Thanh điều khiển và nút hiện lại công cụ phải luôn giữ đúng vị trí căn giữa đáy màn hình, không bị tràn ra ngoài hoặc che khuất nút khác.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Thanh điều khiển `ControlPanel` MUST áp dụng mô hình Thẻ nổi (Floating Card per Clarification Option A) với nền tối đặc `#121212` (độ mờ đục tối thiểu 95%), viền sáng sắc nét (`border: 2px solid rgba(255, 255, 255, 120)`) và hiệu ứng đổ bóng nổi `QGraphicsDropShadowEffect` (màu đen đậm `rgba(0, 0, 0, 200)`, blur radius $\ge 24px$, y-offset $4px$) để tách biệt hoàn toàn khỏi nền ảnh sáng màu hoặc trắng tinh.
- **FR-002**: Các nút bấm trong `ControlPanel` MUST có nền xám đen tối tương phản rõ rệt (`rgba(35, 35, 35, 230)`), viền nút rõ nét và chữ/icon màu trắng tinh (`#FFFFFF`) với độ tương phản đạt tối thiểu 7:1 so với nền nút.
- **FR-003**: Nút "👁️ Hiện thanh công cụ" (`btn_show_panel`) MUST được nâng cấp với kiểu dáng tương phản cao tương đương, có gắn `QGraphicsDropShadowEffect` màu đen xung quanh để hiển thị rõ rệt trên ảnh nền sáng.
- **FR-004**: Thực thể `ViewerSettings` trong Domain và tầng lưu trữ `JsonSettingsRepository` MUST bổ sung 2 trường dữ liệu mới:
  - `is_random: bool` (mặc định: `False`)
  - `show_control_panel: bool` (mặc định: `True`)
- **FR-005**: Hệ thống MUST tự động lưu trạng thái `is_random` vào `settings.json` ngay khi người dùng bấm nút Random trên thanh điều khiển hoặc phím tắt tương ứng.
- **FR-006**: Hệ thống MUST tự động lưu trạng thái `show_control_panel` vào `settings.json` ngay khi người dùng bấm nút Ẩn/Hiện hoặc phím tắt `H`.
- **FR-007**: Khi khởi chạy ứng dụng, hệ thống MUST nạp các thiết lập `is_random` và `show_control_panel` đã lưu để khôi phục chính xác trạng thái của `ControlPanel`, nút `btn_random`, danh sách `Playlist` và nút `btn_show_panel`.
- **FR-008**: Tất cả các thay đổi MUST tuân thủ tuyệt đối cấu trúc Clean Architecture 4 tầng hiện tại (Domain không dính Qt, Use Case điều phối, UI chỉ hiển thị).

### Key Entities

- **ViewerSettings**: Bổ sung `is_random: bool = False` và `show_control_panel: bool = True`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tỷ lệ tương phản của thanh điều khiển và nhãn chữ so với nền ảnh trắng đạt chuẩn thị giác rõ ràng (không xảy ra hiện tượng mờ lóa hoặc chìm màu).
- **SC-002**: 100% các phiên mở lại ứng dụng khôi phục chính xác trạng thái của chế độ Random và trạng thái Ẩn/Hiện thanh điều khiển từ phiên trước đó.
- **SC-003**: Thao tác ẩn/hiện và bật/tắt random phản hồi tức thời (<50ms) và không gây giật lag khung hình trình chiếu.
- **SC-004**: Không có bất kỳ lỗi hồi quy nào đối với các tính năng xem ảnh, zoom, phím tắt hoặc đóng gói PyInstaller.

## Assumptions

- Người dùng mong muốn lưu trạng thái ngay tại thời điểm thao tác (không cần bấm nút "Lưu" riêng biệt).
- Thiết kế Dark Theme hiện tại vẫn là phong cách chủ đạo, chỉ nâng cấp độ đậm nền, viền và hiệu ứng đổ bóng để đảm bảo tương phản.
