# Feature Specification: Tinh Chỉnh Vòng Đời BGM Trong Cài Đặt & Khởi Tạo Âm Lượng

**Feature Branch**: `008-fix-bgm-settings-and-volume`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description:
- "khi đổi link hoặc nguồn nhạc thì mới dừng nhạc khi bấm lưu cài đặt"
- "sửa Lỗi khi bấm tắt cài đặt nó cũng bị tắt nhạc"
- "sửa lỗi âm thanh nhạc, khi bật nhạc lên khi mới mở app thì nó không theo mức âm thanh đã lưu trước đó"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Duy Trì Nhạc Nền Khi Đóng/Hủy Hộp Thoại Cài Đặt (Priority: P1) 🎯 MVP

Là một người dùng đang nghe nhạc nền trong lúc xem ảnh, khi tôi mở hộp thoại Cài đặt lên để xem thông số rồi nhấn nút "Hủy", bấm biểu tượng Đóng (X), hoặc nhấn phím `Esc`, tôi muốn nhạc nền đang phát ngoài màn hình chính tiếp tục phát bình thường, KHÔNG bị tắt đột ngột.

**Why this priority**: Việc đóng/hủy hộp thoại cài đặt không được làm gián đoạn trải nghiệm nghe nhạc liên tục của người dùng ngoài màn hình xem ảnh.

**Independent Test**: Bật nhạc nền ngoài màn hình chính; mở hộp thoại Cài đặt (không bấm nút nghe thử); nhấn nút "Hủy" hoặc phím `Esc`; kiểm tra nhạc nền vẫn tiếp tục phát liền mạch không ngắt quãng.

**Acceptance Scenarios**:

1. **Given** nhạc nền đang phát ngoài màn hình chính và người dùng mở Cài đặt (chưa kích hoạt tính năng Nghe thử), **When** người dùng đóng Cài đặt bằng nút Hủy, dấu X hoặc phím Esc, **Then** nhạc nền vẫn tiếp tục phát bình thường.
2. **Given** người dùng đang trong Cài đặt và ĐÃ BẤM nút "Nghe thử", **When** người dùng đóng Cài đặt, **Then** âm thanh nghe thử phải lập tức dừng lại để tránh phát âm thanh ngầm.

---

### User Story 2 - Giữ Nhạc Phát Liên Tục Khi Lưu Cài Đặt Không Thay Đổi Nguồn Nhạc (Priority: P1)

Là một người dùng đang nghe nhạc nền và mở Cài đặt để chỉnh sửa các thiết lập khác (như thời gian chuyển ảnh, màu nền, hiệu ứng chuyển cảnh), khi tôi nhấn "Lưu", tôi muốn nhạc nền vẫn tiếp tục phát mượt mà, CHỈ dừng hoặc nạp lại khi tôi thực sự thay đổi URL hoặc nguồn phát nhạc.

**Why this priority**: Tránh trải nghiệm khó chịu khi người dùng chỉ muốn đổi tốc độ slideshow hoặc màu nền mà bài nhạc nền lại bị tắt hoặc tải lại từ đầu.

**Independent Test**: Bật nhạc nền đang phát; mở Cài đặt, chỉnh thời gian chuyển ảnh từ 3 giây lên 5 giây (giữ nguyên đường dẫn nhạc); nhấn "Lưu"; kiểm tra bài hát đang phát không bị gián đoạn hay tải lại từ đầu.

**Acceptance Scenarios**:

1. **Given** nhạc nền đang phát ngoài màn hình chính, **When** người dùng lưu cài đặt mà đường dẫn nhạc và nguồn nhạc KHÔNG thay đổi, **Then** nhạc nền tiếp tục phát mà không bị dừng hay tải lại nguồn phát.
2. **Given** nhạc nền đang phát, **When** người dùng thay đổi đường dẫn nhạc sang một link khác rồi bấm "Lưu", **Then** hệ thống dừng bài hát cũ và áp dụng nguồn nhạc mới.
3. **Given** người dùng xóa trắng đường dẫn nhạc rồi bấm "Lưu", **Then** hệ thống dừng nhạc nền đang phát và chuyển trạng thái về chưa cấu hình.

---

### User Story 3 - Áp Dụng Chính Xác Mức Âm Lượng Đã Lưu Ngay Khi Khởi Động Ứng Dụng (Priority: P1)

Là một người dùng đã lưu cấu hình mức âm lượng nhạc nền (ví dụ 25%), khi tôi mở ứng dụng lên trong một phiên làm việc mới và nhấn nút Bật nhạc, tôi muốn âm lượng phát ra loa đúng chính xác 25% như đã lưu, KHÔNG bị phát ở mức âm lượng mặc định (70% hoặc 100%) gây giật mình.

**Why this priority**: Bảo vệ thính giác và sự thoải mái của người dùng khi âm lượng được đồng bộ nhất quán ngay từ đầu phiên làm việc.

**Independent Test**: Đặt âm lượng nhạc nền là 20% trong Cài đặt và đóng ứng dụng; mở lại ứng dụng; nhấn nút "Bật nhạc" ngoài màn hình chính; kiểm tra mức âm lượng phát ra và thanh trượt âm lượng phản ánh đúng giá trị 20%.

**Acceptance Scenarios**:

1. **Given** cấu hình âm lượng đã lưu là $V$ (với $0 \le V \le 100$), **When** ứng dụng khởi động và người dùng bấm phát nhạc ngoài màn hình chính lần đầu tiên, **Then** trình phát nhạc áp dụng mức âm lượng $V$ ngay từ frame âm thanh đầu tiên.
2. **Given** người dùng điều chỉnh âm lượng qua thanh trượt âm lượng trên thanh công cụ option hoặc trong Cài đặt, **When** mức âm lượng được thay đổi, **Then** giá trị mới được lưu trữ và tiếp tục được duy trì ở các phiên khởi động kế tiếp.

---

### Edge Cases

- **Người dùng bấm "Nghe thử" trong Cài đặt rồi sửa link khác**: Âm thanh nghe thử cũ dừng lại; khi bấm "Lưu", nguồn mới được áp dụng và nhạc ngoài màn hình chính dừng bài cũ để chuẩn bị cho nguồn mới.
- **Người dùng chỉnh thanh trượt âm lượng về 0%**: Ứng dụng phải duy trì mức 0% (tắt tiếng) khi khởi động lại phiên mới, không tự ý nhảy về mức mặc định.
- **Người dùng chỉ thêm khoảng trắng vào link nhạc hiện tại**: Hệ thống tự động chuẩn hóa chuỗi và nhận diện link không thay đổi về mặt nội dung, không ngắt nhạc không cần thiết.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Khi đóng hộp thoại Cài đặt (thông qua nút Hủy, phím Esc, hoặc nút đóng cửa sổ), hệ thống MUST CHỈ dừng âm thanh nếu người dùng đang trong trạng thái "Nghe thử", TUYỆT ĐỐI KHÔNG làm dừng nhạc nền đang phát của màn hình trình chiếu chính.
- **FR-002**: Khi lưu cài đặt từ hộp thoại Cài đặt, hệ thống MUST so sánh nguồn phát nhạc mới (URL và nguồn) với nguồn phát nhạc trước khi mở hộp thoại:
  - Nếu nguồn phát KHÔNG thay đổi: Hệ thống giữ nguyên trạng thái phát của nhạc nền (tiếp tục phát nếu đang phát).
  - Nếu nguồn phát ĐÃ thay đổi hoặc bị xóa: Hệ thống mới thực hiện dừng bài hát cũ và cập nhật cấu hình mới.
- **FR-003**: Khi ứng dụng khởi động từ phiên làm việc mới, hệ thống MUST khởi tạo âm lượng của trình phát nhạc bằng đúng giá trị `bgm_volume` được nạp từ tệp cấu hình lưu trữ, đảm bảo không sử dụng âm lượng mặc định tạm thời.
- **FR-004**: Khi phương thức phát nhạc được gọi (`play()`), hệ thống MUST đảm bảo âm lượng hiện thời của trình phát khớp với giá trị âm lượng đã cấu hình trước khi kích hoạt luồng phát.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% các lần đóng/hủy hộp thoại Cài đặt khi đang nghe nhạc ngoài màn hình chính (không bấm nghe thử) sẽ giữ nhạc tiếp tục phát, tỷ lệ ngắt nhạc ngoài ý muốn là 0%.
- **SC-002**: 100% các lần lưu Cài đặt chỉ đổi các thông số không liên quan đến nhạc (thời gian chuyển ảnh, màu nền, hiệu ứng) sẽ không làm gián đoạn bài nhạc đang phát.
- **SC-003**: 100% các phiên khởi động mới, âm lượng phát ra khi bấm Bật nhạc lần đầu tiên khớp tuyệt đối với giá trị đã lưu trong cấu hình (sai số 0%).

---

## Assumptions

- Mức âm lượng được lưu trữ trong khoảng từ 0 đến 100 dạng số nguyên.
- Trình phát nhạc cục bộ có cơ chế điều chỉnh âm lượng độc lập với âm lượng tổng của hệ điều hành.

