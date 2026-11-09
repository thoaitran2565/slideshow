# Feature Specification: Tinh Chỉnh Vòng Đời Nhạc Nền, Lớp Phủ Chống Click Xuyên & Tối Ưu Mượt Mà Hiệu Ứng Zoom Fade

**Feature Branch**: `006-bgm-lifecycle-and-zoom-polish`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "Loại bỏ ô kích hoạt nhạc nền khi trình chiếu; Không gắn kết việc bật tắt nhạc với play pause của slide trình chiếu mà hoạt động độc lập; chuột phải vào nút bật tắt nhạc hiện lên thanh điều khiển âm thanh và phải cho bấm ra ngoài để tắt nhưng không bị bấm vào nền hay các nút: cái này có thể giả lập một lớp phủ trong suốt khi nhấn ra ngoài thực chất là nhấn lên lớp phủ; khi bấm nút bật nhạc nếu đang load nhạc thì cho nút hiện loading để người dùng biết là đang đợi load, trong lúc load thì không cho bấm thêm vào nút bật nhạc nữa và không cho tùy chỉnh trong tab nhạc nền trong cài đặt (tab Nhạc nền cũng hiện loading luôn), đặt giới hạn thời gian load nếu quá lâu thì báo lỗi và chuyển trạng thái về ban đầu để có thể thao tác tiếp hoặc chỉnh sửa link; khi thay đổi link hoặc bấm nghe thử trong cài đặt thì tắt nhạc nền nếu đang phát; Chế độ hòa trộn (Zoom fade) hiện tại chưa được mượt lắm tại vì mỗi ảnh có kích thước khác nhau nên khi chuyển qua ảnh đang hiển thị nhỏ hơn hoặc lớn hơn bình thường rồi mới thu phóng lại cho phù hợp với màn hình nên vẫn hơi giật"

## Clarifications

### Session 2026-11-09
- Q: Khi việc nạp nhạc nền YouTube bị quá thời gian chờ (15 giây timeout) hoặc gặp lỗi mạng/link hỏng, hệ thống nên hiển thị thông báo lỗi bằng hình thức nào để vừa rõ ràng vừa không làm gián đoạn trải nghiệm xem ảnh của người dùng? → A: Hiển thị thông báo trạng thái/tooltip màu đỏ trực tiếp tại nút BGM (Non-intrusive notification), không bật popup modal chặn màn hình; cập nhật thông báo lỗi chi tiết trong tab Nhạc Nền của hộp thoại Cài đặt.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Tách Biệt Độc Lập Vòng Đời Nhạc Nền & Hợp Nhất Trải Nghiệm Cài Đặt (Priority: P1) 🎯 MVP

Là một người dùng xem ảnh, tôi muốn việc phát nhạc nền hoạt động độc lập hoàn toàn với việc Tạm dừng / Tiếp tục của trình chiếu slideshow (khi tôi tạm dừng ảnh để ngắm một bức ảnh đẹp thì nhạc vẫn tiếp tục du dương), và tôi muốn loại bỏ ô checkbox kích hoạt rườm rà trong Cài đặt để việc bật/tắt nhạc tập trung duy nhất ở nút điều khiển trên thanh công cụ. Đồng thời khi tôi sửa link hoặc bấm nghe thử trong cài đặt, nhạc nền đang phát ngoài màn hình phải tự động tắt để tránh bị chồng chéo âm thanh.

**Why this priority**: Giải phóng âm nhạc khỏi sự ràng buộc cứng nhắc với tiến trình chuyển slide, tạo trải nghiệm nghe nhìn tự nhiên và trực quan nhất cho người dùng.

**Independent Test**: Bật nhạc nền đang phát; bấm Phím cách (Space) để Pause slideshow; xác nhận slide dừng nhưng âm thanh vẫn tiếp tục phát mượt mà. Mở Cài đặt, bấm "Nghe thử" hoặc sửa link; xác nhận nhạc nền slideshow bên ngoài tự động tắt tức thì.

**Acceptance Scenarios**:

1. **Given** nhạc nền đang phát, **When** người dùng bấm Tạm dừng slideshow (Space hoặc nút Pause), **Then** chu kỳ chuyển ảnh dừng lại nhưng nhạc nền vẫn tiếp tục phát bình thường không bị gián đoạn.
2. **Given** người dùng mở hộp thoại Cài đặt (`SettingsDialog`), **Then** không còn xuất hiện ô checkbox "Kích hoạt nhạc nền khi trình chiếu"; người dùng chỉ cần nhập link YouTube và bấm Lưu/Đóng hoặc Nghe thử.
3. **Given** nhạc nền đang phát ngoài màn hình chính, **When** người dùng bấm nút "▶ Nghe Thử" hoặc chỉnh sửa nội dung ô nhập link YouTube trong Cài đặt, **Then** hệ thống tự động tắt luồng nhạc nền slideshow đang phát ngoài màn hình chính để phát âm thanh kiểm tra.

---

### User Story 2 - Trạng Thái Đang Tải Nhạc (Loading State) Kèm Cơ Chế Giới Hạn Thời Gian An Toàn (Priority: P1)

Là một người dùng xem ảnh có kết nối mạng chậm hoặc đang kết nối bài nhạc YouTube dài, tôi muốn khi bấm nút "Bật nhạc", nút này chuyển sang trạng thái "Đang tải..." (loading) và tạm thời bị khóa không cho bấm tiếp, đồng thời tab Nhạc Nền trong Cài đặt cũng hiển thị trạng thái đang tải và khóa tùy chỉnh, kèm theo giới hạn thời gian chờ an toàn (Timeout 15 giây) để nếu mạng treo thì tự động báo lỗi và đưa nút về lại trạng thái ban đầu, tránh bị treo ứng dụng hoặc spam thao tác.

**Why this priority**: Cung cấp phản hồi thị giác rõ ràng cho thao tác bất đồng bộ qua mạng, ngăn ngừa xung đột luồng và giải cứu trạng thái giao diện khi gặp sự cố kết nối.

**Independent Test**: Bấm nút "🎵 Bật nhạc"; nút đổi ngay sang `"⏳ Đang tải..."` và bị vô hiệu hóa; trong lúc đang tải mở Cài đặt thấy tab Nhạc Nền báo đang kết nối và tạm khóa controls; nếu ngắt mạng thử nghiệm, sau 15 giây hệ thống phát thông báo lỗi, nút phục hồi về `"🎵 Bật nhạc"` cho phép bấm lại.

**Acceptance Scenarios**:

1. **Given** người dùng bấm nút "🎵 Bật nhạc", **When** hệ thống bắt đầu trích xuất luồng âm thanh YouTube, **Then** nút BGM lập tức chuyển tiêu đề thành `"⏳ Đang tải..."`, bị vô hiệu hóa click chuột (`disabled`) để chống bấm lặp lại.
2. **Given** quá trình nạp nhạc đang diễn ra, **When** người dùng mở hộp thoại Cài đặt (tab Nhạc Nền), **Then** giao diện tab Nhạc Nền hiển thị nhãn `"⏳ Đang tải nhạc..."` và tạm thời vô hiệu hóa ô nhập link và nút nghe thử.
3. **Given** tiến trình nạp nhạc vượt quá 15 giây hoặc gặp lỗi mạng / trích xuất URL thất bại, **When** hết thời gian timeout, **Then** hệ thống hủy tiến trình nạp, hiển thị thông báo lỗi rõ ràng và tự động chuyển trạng thái nút BGM và tab Cài đặt về lại ban đầu (`"🎵 Bật nhạc"`) để người dùng có thể thao tác tiếp hoặc chỉnh sửa link.
4. **Given** tiến trình nạp nhạc thành công, **When** âm thanh bắt đầu phát ra loa, **Then** nút BGM đổi sang `"🔇 Tắt nhạc"` và mở khóa tương tác bình thường.

---

### User Story 3 - Lớp Phủ Chống Click Xuyên Khi Đóng Popup Âm Lượng Chuột Phải (Priority: P2)

Là một người xem ảnh đang mở popup thanh trượt âm lượng bằng chuột phải, tôi muốn khi nhấp chuột ra ngoài để đóng popup, cú nhấp chuột đó chỉ dùng để đóng popup mà không vô tình kích hoạt trúng các nút khác bên dưới (như Pause, Next, Random) hay đổi ảnh trong khung nhìn.

**Why this priority**: Tránh các thao tác nhầm lẫn tai hại (vô tình bấm xóa ảnh, bấm chuyển slide hoặc kích hoạt tính năng khác khi người dùng chỉ muốn đóng thanh âm lượng).

**Independent Test**: Nhấp chuột phải vào nút BGM để mở thanh âm lượng nổi; rê chuột nhấp vào nút "⏸ Pause" hoặc vào vùng canvas ảnh; popup âm lượng biến mất, nhưng slideshow KHÔNG bị đổi trạng thái Pause/Play và ảnh KHÔNG bị phóng to/chuyển đổi.

**Acceptance Scenarios**:

1. **Given** popup chỉnh âm lượng nhanh đang hiển thị nổi, **When** người dùng nhấp chuột vào bất kỳ vị trí nào bên ngoài popup, **Then** lớp phủ trong suốt (Transparent Backdrop Overlay) hấp thụ trọn vẹn cú nhấp chuột đó, đóng popup âm lượng và không cho sự kiện chuột xuyên thấu xuống các widget hoặc canvas ảnh bên dưới.
2. **Given** popup âm lượng đã đóng, **When** người dùng nhấp chuột tiếp theo vào các nút trên màn hình, **Then** các nút hoạt động bình thường trở lại.

---

### User Story 4 - Chuẩn Hóa Khung Hình Mượt Mà Cho Hiệu Ứng Chuyển Cảnh Zoom Fade (Priority: P2)

Là một người xem ảnh có bộ sưu tập nhiều bức ảnh với kích thước và độ phân giải chênh lệch nhau (ví dụ ảnh 4K dọc xen kẽ ảnh màn hình ngang), tôi muốn hiệu ứng chuyển cảnh "Phóng to hòa trộn" (Zoom Fade) chuyển động mượt mà, đồng tâm và không bị giật cục kích thước trong suốt quá trình hòa tan hình ảnh.

**Why this priority**: Nâng cao trải nghiệm thị giác lên mức cao cấp, loại bỏ lỗi giật hình do khác biệt độ phân giải giữa các bức ảnh.

**Independent Test**: Chọn hiệu ứng "Zoom Fade" trong Cài đặt; duyệt chuyển tiếp liên tục giữa các ảnh có kích thước rất khác nhau (ảnh dọc độ phân giải thấp sang ảnh ngang siêu nét); hai bức ảnh hòa quyện êm ái, tỷ lệ co giãn đồng nhất từ đầu đến cuối hiệu ứng mà không bị giật nảy khung hình.

**Acceptance Scenarios**:

1. **Given** hiệu ứng chuyển cảnh là Zoom Fade, **When** ảnh mới chuẩn bị hiển thị, **Then** hệ thống tính toán trước ma trận căn chỉnh vừa vặn khung nhìn (`fitInView`) cho ảnh mới trước khi hoạt ảnh bắt đầu, đảm bảo ảnh mới nằm đúng tỷ lệ và vị trí trung tâm ngay từ frame đầu tiên.
2. **Given** hoạt ảnh Zoom Fade đang diễn ra trong 450ms, **When** ảnh cũ mờ dần và phóng to nhẹ ($1.0x \rightarrow 1.08x$) trong khi ảnh mới tăng độ mờ ($0.0 \rightarrow 1.0$) và thu phóng êm ái về chuẩn ($0.95x \rightarrow 1.0x$), **Then** tốc độ khung hình đạt 60 FPS ổn định, không xuất hiện hiện tượng biến dạng tỷ lệ hoặc giật nảy kích thước.

---

### Edge Cases

- **Người dùng bấm liên tục vào nút BGM khi mạng đang kết nối**: Nút bị disabled ngay khi bấm lần 1 nên các cú click tiếp theo bị chặn hoàn toàn, không tạo ra nhiều luồng nạp stream song song.
- **Đóng ứng dụng hoặc mở hộp thoại khác khi nhạc đang ở trạng thái loading**: Timer timeout và luồng nền `yt-dlp` được hủy an toàn (terminate/quit), không gây treo tiến trình khi tắt app.
- **Cửa sổ ứng dụng bị co giãn kích thước (Resize window) khi popup âm lượng đang mở**: Lớp phủ trong suốt tự động bao phủ trọn vẹn diện tích cửa sổ mới hoặc tự động đóng popup an toàn.
- **Chuyển slide liên tục tốc độ cao khi đang dùng Zoom Fade**: Hoạt ảnh cũ bị hủy ngay lập tức và đưa ảnh vào vị trí ổn định trước khi kích hoạt hoạt ảnh mới, ngăn ngừa hiện tượng chồng đè ma trận biến đổi.

## Requirements *(mandatory)*

### Functional Requirements

#### A. Độc Lập Vòng Đời Nhạc Nền & Ngăn Ngừa Xung Đột
- **FR-001**: Hệ thống MUST tách rời hoàn toàn vòng đời của trình phát nhạc nền (`ManageBgmUseCase`) khỏi trạng thái Tạm dừng / Tiếp tục (`toggle_play_pause`) của trình chiếu ảnh.
- **FR-002**: Hệ thống MUST loại bỏ trường/checkbox kích hoạt nhạc nền tự động trong Cài đặt (`SettingsDialog`), chuyển quyền điều khiển phát/dừng nhạc nền trực tiếp và duy nhất qua nút BGM trên thanh `ControlPanel`.
- **FR-003**: Khi người dùng bấm nút "▶ Nghe Thử" hoặc chỉnh sửa chuỗi URL YouTube trong `SettingsDialog`, nếu nhạc nền slideshow đang phát ngoài màn hình chính, hệ thống MUST tự động dừng luồng phát ngoài màn hình chính trước khi xử lý luồng âm thanh mới.

#### B. Trạng Thái Loading Nạp Nhạc & Giới Hạn Thời Gian Chờ An Toàn
- **FR-004**: Khi người dùng nhấn nút BGM để phát nhạc, hệ thống MUST lập tức chuyển nút sang trạng thái `LOADING` với nhãn `"⏳ Đang tải..."` và vô hiệu hóa (`setEnabled(False)`) nút bấm.
- **FR-005**: Trong suốt thời gian trạng thái `LOADING`, tab Nhạc Nền trong `SettingsDialog` MUST hiển thị thông báo trạng thái `"⏳ Đang tải nhạc..."` và tạm thời khóa các thao tác sửa đổi link hoặc nghe thử.
- **FR-006**: Hệ thống MUST cài đặt cơ chế đếm ngược thời gian chờ tối đa (Safety Timeout: 15 giây) cho việc nạp nhạc. Nếu sau 15 giây luồng âm thanh chưa sẵn sàng hoặc trích xuất thất bại:
  - Hệ thống MUST tự động hủy tác vụ nạp.
  - Hiển thị thông báo lỗi thân thiện cho người dùng.
  - Phục hồi trạng thái nút BGM về lại ban đầu (`"🎵 Bật nhạc"`, `setEnabled(True)`) và mở khóa tab Cài đặt.
- **FR-007**: Khi luồng nhạc nạp thành công và bắt đầu phát, hệ thống MUST chuyển trạng thái nút BGM sang `"🔇 Tắt nhạc"` và bật lại tính tương tác.

#### C. Lớp Phủ Chống Click Xuyên Cho Popup Âm Lượng
- **FR-008**: Khi Quick Volume Popup xuất hiện sau thao tác nhấp chuột phải trên nút BGM, hệ thống MUST kích hoạt một lớp phủ trong suốt (Transparent Modal Overlay Backdrop) trải rộng trên toàn bộ cửa sổ ứng dụng.
- **FR-009**: Cú nhấp chuột bất kỳ rơi vào vùng ngoài của Quick Volume Popup MUST bị lớp phủ này chặn và hấp thụ (consume event), chỉ thực hiện nhiệm vụ ẩn popup âm lượng và giải phóng lớp phủ, TUYỆT ĐỐI KHÔNG chuyển phát sự kiện chuột xuống các nút hoặc canvas ảnh bên dưới.

#### D. Tối Ưu Hóa Mượt Mà Hiệu Ứng Zoom Fade
- **FR-010**: Bộ xử lý hiệu ứng chuyển cảnh `ZoomFadeTransition` MUST tiền xử lý (pre-fit & normalize) kích thước và tâm hiển thị của ảnh mới (`incoming_item`) cho vừa khít với khung nhìn hiển thị trước khi kích hoạt hoạt ảnh phóng to mờ dần.
- **FR-011**: Hoạt ảnh Zoom Fade MUST áp dụng hoạt ảnh biến đổi đồ họa liên tục quanh tâm khung nhìn chuẩn hóa, đảm bảo tỷ lệ co giãn đồng nhất không phụ thuộc vào độ chênh lệch kích thước pixel giữa 2 ảnh liên tiếp.

### Key Entities

- **BgmLoadingState**: Biểu diễn các trạng thái hoạt động của BGM: `IDLE_STOPPED`, `LOADING`, `PLAYING`, `ERROR`.
- **BackdropOverlay**: Lớp phủ sự kiện trong suốt kiểm soát hành vi click outside không xuyên thấu.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% các thao tác Tạm dừng / Tiếp tục trình chiếu ảnh không làm gián đoạn bài nhạc nền đang phát.
- **SC-002**: Nút BGM hiển thị trạng thái `"⏳ Đang tải..."` và khóa click tức thời (< 30ms) sau khi bấm; thời gian timeout giới hạn chính xác trong 15 giây bảo vệ an toàn hệ thống.
- **SC-003**: 100% cú nhấp chuột đóng popup âm lượng ngoài màn hình không bị kích hoạt xuyên thấu vào các nút điều khiển hoặc canvas ảnh bên dưới.
- **SC-004**: Hiệu ứng Zoom Fade vận hành mượt mà ở tốc độ 60 FPS, không có hiện tượng giật tỷ lệ hay lệch kích thước khi chuyển đổi giữa các ảnh chênh lệch độ phân giải.

## Assumptions

- Thời gian timeout 15 giây là khoảng thời gian công thái học hợp lý cho một kết nối mạng băng thông thấp trích xuất audio stream YouTube qua `yt-dlp`.
- Lớp phủ chống click xuyên sử dụng cơ chế `QWidget` trong suốt bắt `mousePressEvent` trực tiếp trong kiến trúc PyQt6.

