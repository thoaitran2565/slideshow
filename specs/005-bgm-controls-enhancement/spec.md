# Feature Specification: Nâng Cấp Điều Khiển Nhạc Nền (Live Volume, Quick Popup, BGM Label & Source Protection)

**Feature Branch**: `005-bgm-controls-enhancement`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "thanh chỉnh âm thanh cần cập nhật lại âm lượng khi đang bật nút test nhạc luôn, hiện tại thì nó chỉ thay đổi khi bấm dừng và bật lại thôi; nút bật nhạc ở thanh option bên dưới cần để title là bật nhạc/tắt nhạc; khi nhấn chuột phải vào nút bât/tắt nhạc dưới thanh option thì cho hiện lên nút chỉnh âm lượng và cập nhật âm thanh trong lúc đang phát luôn, không cần phải tắt và bật lại; Các nguồn phát nhạc trong cài đặt, cái nào chưa có thì tạm thời chưa cho bấm vào"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cập Nhật Âm Lượng Nhạc Nền Thời Gian Thực (Live Volume Adjustment) (Priority: P1) 🎯 MVP

Là một người dùng đang nghe thử bài nhạc trong hộp thoại Cài đặt hoặc đang xem trình chiếu ảnh với nhạc nền, tôi muốn âm lượng nhạc thay đổi ngay tức thì khi tôi di chuyển thanh trượt âm lượng (không cần phải bấm tạm dừng rồi phát lại), để tôi có thể căn chỉnh mức âm lượng vừa tai một cách thuận tiện và chính xác.

**Why this priority**: Trực tiếp sửa lỗi trải nghiệm âm thanh gián đoạn, mang lại phản hồi thính giác tức thời khi người dùng tương tác với thanh trượt âm lượng.

**Independent Test**: Mở Cài đặt, bấm "Nghe thử", trong lúc âm thanh đang phát tiến hành kéo thanh trượt âm lượng từ 100% xuống 20%; âm lượng loa giảm dần ngay theo từng nấc di chuyển của con trỏ chuột mà âm thanh không bị ngắt quãng.

**Acceptance Scenarios**:

1. **Given** người dùng đang bấm "Nghe thử" trong hộp thoại Cài đặt và âm thanh đang phát, **When** người dùng kéo thanh trượt âm lượng, **Then** âm lượng phát ra thay đổi ngay tức thời tương ứng với vị trí thanh trượt theo thời gian thực (real-time).
2. **Given** nhạc nền đang phát trong lúc trình chiếu ảnh, **When** người dùng thay đổi âm lượng trong cài đặt hoặc qua phím tắt / popup, **Then** âm lượng loa cập nhật ngay lập tức mà bài hát không bị dừng hoặc giật hạt âm thanh.
3. **Given** người dùng điều chỉnh âm lượng, **When** đóng hoặc lưu cài đặt, **Then** mức âm lượng mới được ghi nhớ bền vững vào cấu hình người dùng (`settings.json`).

---

### User Story 2 - Popup Chỉnh Âm Lượng Nhanh Bằng Chuột Phải Trên Thanh Điều Khiển (Priority: P1)

Là một người xem ảnh đang thưởng thức slideshow ở chế độ toàn màn hình hoặc cửa sổ, tôi muốn có thể nhấp chuột phải vào nút Nhạc nền (🎵/🔇) trên thanh điều khiển nổi (Control Panel) để xuất hiện ngay một thanh trượt chỉnh âm lượng nhanh và điều chỉnh âm thanh trực tiếp tại chỗ, không cần phải mở hộp thoại Cài đặt.

**Why this priority**: Cung cấp lối tắt điều khiển âm lượng công thái học ngay trên màn hình chính, tương tự hành vi của biểu tượng loa trên thanh tác vụ hệ điều hành.

**Independent Test**: Nhấp chuột phải vào nút BGM trên thanh Control Panel; một thanh trượt âm lượng nhỏ gọn xuất hiện ngay phía trên nút; kéo thanh trượt để chỉnh âm lượng bài nhạc đang phát; nhấp chuột ra ngoài để đóng popup.

**Acceptance Scenarios**:

1. **Given** thanh điều khiển nổi đang hiển thị, **When** người dùng nhấp chuột phải (Right-Click) vào nút BGM, **Then** một popup / thanh trượt âm lượng nhanh (Quick Volume Popup) xuất hiện mượt mà ngay trên nút bấm.
2. **Given** popup âm lượng đang mở, **When** người dùng kéo thanh trượt từ 0% đến 100%, **Then** âm lượng nhạc nền đang phát thay đổi theo thời gian thực ngay lập tức.
3. **Given** popup âm lượng đang hiển thị, **When** người dùng nhấp chuột ra ngoài vùng popup hoặc nhấp chuột phải lại vào nút, **Then** popup tự động ẩn đi và lưu lại giá trị âm lượng hiện hành.
4. **Given** người dùng mở popup khi chưa có nhạc hoặc đang tắt nhạc, **When** điều chỉnh âm lượng, **Then** mức âm lượng đã chọn vẫn được lưu và áp dụng cho lần phát tiếp theo.

---

### User Story 3 - Chuẩn Hóa Nhãn Nút BGM & Khóa Nguồn Nhạc Chưa Khả Dụng (Priority: P2)

Là một người dùng xem ảnh, tôi muốn nút nhạc trên thanh điều khiển có chú thích rõ ràng bằng chữ ("Bật nhạc" khi đang tắt và "Tắt nhạc" khi đang bật) thay vì chỉ có biểu tượng, và trong mục Cài đặt chỉ cho phép chọn nguồn phát đã hoạt động (YouTube), vô hiệu hóa các nguồn chưa phát triển (Spotify, Local file...) để tránh hiểu lầm hoặc bấm nhầm gây lỗi.

**Why this priority**: Nâng cao tính rõ ràng thị giác và đảm bảo tính toàn vẹn của giao diện, ngăn ngừa thao tác không hợp lệ.

**Independent Test**: Kiểm tra nút BGM trên thanh Control Panel thấy hiển thị đúng nhãn và tooltip "Bật nhạc" (khi tắt) và "Tắt nhạc" (khi bật); mở Cài đặt và mở danh sách nguồn nhạc, thấy các mục chưa hỗ trợ bị mờ đi và không thể bấm chọn.

**Acceptance Scenarios**:

1. **Given** nhạc nền đang ở trạng thái tắt, **When** người dùng nhìn vào nút BGM trên thanh điều khiển, **Then** nút hiển thị rõ ràng nhãn hoặc tooltip mang nội dung "Bật nhạc".
2. **Given** nhạc nền đang ở trạng thái bật, **When** người dùng nhìn vào nút BGM trên thanh điều khiển, **Then** nút chuyển đổi hiển thị nhãn hoặc tooltip mang nội dung "Tắt nhạc".
3. **Given** người dùng mở hộp thoại Cài đặt và nhấp vào hộp chọn "Nguồn phát" (Music Source), **Then** tùy chọn "YouTube" có thể chọn bình thường; các tùy chọn chưa phát triển (ví dụ: "Spotify", "Tệp cục bộ / Ổ cứng") bị vô hiệu hóa (disabled / không cho bấm chọn) và có nhãn chú thích rõ (ví dụ: "(Sắp ra mắt)").

---

### Edge Cases

- **Kéo thanh trượt âm lượng về 0%**: Hệ thống tắt tiếng (Mute) bài nhạc an toàn nhưng vẫn duy trì luồng phát; khi kéo lên > 0% âm thanh phát lại bình thường.
- **Nhấp chuột phải vào nút BGM khi thanh Control Panel sắp chạm đáy màn hình**: Popup âm lượng tự động định vị nổi lên phía trên nút, không bị che khuất hoặc tràn ra ngoài mép màn hình.
- **Kéo thanh trượt âm lượng liên tục với tần suất cao (High-frequency slider dragging)**: Bộ điều khiển âm lượng cập nhật mượt mà không gây tắc nghẽn luồng giao diện (UI lag) và chỉ ghi đĩa `settings.json` khi người dùng thả chuột (sliderReleased) hoặc đóng popup.
- **Nguồn nhạc chưa cấu hình khi nhấp chuột phải**: Popup âm lượng vẫn hiển thị để người dùng có thể đặt trước mức âm lượng mặc định trước khi nhập link YouTube.

## Requirements *(mandatory)*

### Functional Requirements

#### A. Cập Nhật Âm Lượng Trực Tiếp (Live Real-Time Volume)
- **FR-001**: Hệ thống MUST kết nối sự kiện thay đổi của thanh trượt âm lượng (`valueChanged`) trong `SettingsDialog` trực tiếp tới phương thức điều chỉnh âm lượng của trình phát nhạc (`set_volume`), đảm bảo thay đổi mức âm thanh ngay tức thì trong lúc đang nghe thử ("Nghe thử") hoặc đang phát slideshow mà không cần phải dừng và phát lại.
- **FR-002**: Trình phát nhạc (`QtMusicPlayer`) MUST cập nhật ngay thuộc tính âm lượng của `QAudioOutput` khi nhận lệnh `set_volume(volume)` bất kể trình phát đang ở trạng thái `PlayingState`, `PausedState` hay `StoppedState`.

#### B. Quick Volume Popup Trên Thanh Điều Khiển
- **FR-003**: Nút BGM trên thanh điều khiển nổi (`ControlPanel`) MUST hỗ trợ bắt sự kiện nhấp chuột phải (Right-Click / Context Menu Event).
- **FR-004**: Khi nhấp chuột phải vào nút BGM, hệ thống MUST hiển thị một widget popup nhỏ gọn chứa thanh trượt âm lượng (0% - 100%) kèm nhãn phần trăm hiển thị trực quan.
- **FR-005**: Thao tác kéo thanh trượt trong popup MUST cập nhật âm lượng của bài nhạc đang phát theo thời gian thực (live update) và đồng bộ trạng thái cấu hình âm lượng trong ứng dụng.
- **FR-006**: Popup âm lượng MUST tự động đóng khi người dùng nhấp chuột ra ngoài phạm vi popup (Click outside) hoặc khi nút BGM được nhấp chuột phải lần nữa.

#### C. Nhãn Nút BGM & Bảo Vệ Lựa Chọn Nguồn
- **FR-007**: Nút BGM trên thanh điều khiển MUST hiển thị tiêu đề và tooltip tương ứng với trạng thái phát:
  - Khi nhạc đang tắt: Văn bản/Tooltip hiển thị "Bật nhạc" (kèm icon 🎵).
  - Khi nhạc đang bật: Văn bản/Tooltip hiển thị "Tắt nhạc" (kèm icon 🔇).
- **FR-008**: Trong hộp thoại Cài đặt (`SettingsDialog`), danh sách lựa chọn nguồn phát (ComboBox):
  - Nguồn "YouTube" là nguồn hợp lệ, cho phép người dùng lựa chọn và sử dụng.
  - Các nguồn chưa phát triển (như "Spotify", "Tệp trên máy / Ổ đĩa") MUST được thiết lập ở trạng thái không thể chọn (Disabled item), có thể đính kèm hậu tố `(Sắp ra mắt)` để định hướng người dùng.

### Key Entities

- **BgmVolumeState**: Biểu diễn mức âm lượng hiện hành (`volume: int` từ 0 đến 100).
- **BgmControlDisplay**: Biểu diễn trạng thái hiển thị của nút BGM (`is_playing: bool`, `display_text: str`, `tooltip: str`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Thao tác di chuyển thanh trượt âm lượng phản hồi độ lớn âm thanh ra loa ngay lập tức với độ trễ cảm nhận được dưới 50ms, không cần ngắt quãng hoặc khởi động lại luồng âm thanh.
- **SC-002**: 100% người dùng có thể nhấp chuột phải vào nút BGM để mở thanh trượt âm lượng nhanh và điều chỉnh âm thanh thành công ngay trên màn hình xem ảnh trong vòng dưới 2 giây.
- **SC-003**: 100% các nguồn nhạc chưa khả dụng được vô hiệu hóa triệt để, ngăn chặn hoàn toàn việc người dùng chọn nhầm nguồn rỗng gây lỗi hệ thống.
- **SC-004**: Tiêu đề và chú thích nút BGM phản ánh chính xác 100% trạng thái bật/tắt của hệ thống âm thanh mọi lúc.

## Assumptions

- Việc điều chỉnh âm lượng chỉ tác động lên bộ phát âm thanh nội bộ của ứng dụng (`QAudioOutput`), không can thiệp vào âm lượng tổng của toàn hệ điều hành Windows.
- Popup âm lượng nhanh sử dụng ngôn ngữ thiết kế Dark Theme đồng bộ với thanh điều khiển nổi và hộp thoại cài đặt.
- Tần suất lưu cấu hình âm lượng vào đĩa (`settings.json`) được gộp lại khi kết thúc thao tác kéo chuột để tránh ghi đĩa liên tục gây lãng phí tài nguyên I/O.

