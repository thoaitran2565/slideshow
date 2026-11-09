# Feature Specification: Nhạc Nền Đa Nguồn (YouTube), Xoay & Lật Ảnh, Đa Hiệu Ứng Chuyển Cảnh

**Feature Branch**: `004-bgm-transform-transitions`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "Thêm tính năng phát nhạc nền: tính năng này có nhiều option với nhiều phương thức để phát nhạc như phát từ youtube, spotify, file ô cứng hay cách thức khác, vì mỗi cái sẽ có cách để phát nhạc khác nhau nên cần thiết kế riêng cho từng cái, trước tiên chỉ cần thiết kế cho nền tảng youtube thôi còn những cái option khác thì để phát triển sau nên phải thiết kế cấu trúc và logic làm sao để có thể mở rộng cho sau này. Thêm tính năng xoay và lật ảnh: vì ảnh tải từ điện thoại hoặc các trang web nó có thể bị ngược hoặc xoay ngang nên cần có các tính năng này để tăng trải nghiệm người dùng. Thêm tính năng chọn hiệu ứng chuyển động khi chuyển đổi ảnh/slide: cho chọn trong cài đặt hiển thị 5 tùy chọn hiệu ứng và cũng thiết kế để có thể mở rộng thêm nhiều hiệu ứng cho sau này."

## Clarifications

### Session 2026-11-09
- Q: Trạng thái xoay và lật ảnh nên được ghi nhớ theo từng bức ảnh trong suốt phiên làm việc (Session Memory) hay tự động đặt lại về mặc định mỗi khi chuyển sang ảnh khác? → A: Ghi nhớ trong phiên (Session Cache): duy trì góc xoay và lật của từng ảnh trong bộ nhớ đệm suốt phiên làm việc hiện tại, tự động dọn sạch khi đóng ứng dụng, không sửa đổi tệp gốc.
- Q: Khi người dùng duyệt ảnh lùi lại (bấm phím mũi tên Trái hoặc nút Prev), các hiệu ứng chuyển động dạng trượt (Slide Left / Slide Right) nên tự động đảo chiều chuyển động theo hướng duyệt hay luôn giữ cố định hướng đã chọn trong cài đặt? → A: Tự động đảo chiều (Adaptive Direction): khi bấm Next hoặc tự động thì trượt theo hướng đã cấu hình, khi bấm Prev lùi ảnh thì tự động đảo ngược hướng trượt tương ứng để tạo cảm giác lật trang tự nhiên.
- Q: Nhạc nền nên bắt đầu phát khi nào và điều khiển ra sao trên giao diện? → A: Tích hợp nút Bật/Tắt nhạc (🎵/🔇) trực tiếp trên thanh điều khiển nổi (ControlPanel). Nếu nguồn nhạc chưa sẵn sàng hoặc người dùng chưa nhập link/video, bấm nút sẽ tự động mở hộp thoại Cài đặt (SettingsDialog). Trong Cài đặt có thêm nút "Nghe thử" (Test Audio) để chạy thử nhạc và hiển thị thông báo trạng thái/lỗi nếu link không tải được.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Phát Nhạc Nền Từ Nguồn Mở Rộng (Nền Tảng YouTube) (Priority: P1)

Là một người dùng xem trình chiếu ảnh kỷ niệm hoặc nghệ thuật, tôi muốn ứng dụng có thể phát nhạc nền đồng điệu (bắt đầu với nguồn âm thanh trực tuyến từ YouTube) trong khi các bức ảnh đang trình chiếu, để nâng cao cảm xúc và sự hấp dẫn của buổi chiếu ảnh, đồng thời kiến trúc hệ thống sẵn sàng mở rộng các nguồn nhạc khác (Spotify, tệp ổ cứng) trong tương lai.

**Why this priority**: Âm nhạc là yếu tố quyết định nâng tầm trải nghiệm trình chiếu từ một công cụ xem ảnh tĩnh thành một không gian thưởng thức đa phương tiện sống động.

**Independent Test**: Trong hộp thoại Cài đặt, bật tính năng Nhạc nền, chọn nguồn "YouTube", dán đường dẫn (URL) hoặc mã video YouTube và bấm Lưu; ứng dụng tự động phát nhạc nền khi trình chiếu, có thể tạm dừng/tiếp tục cùng trình chiếu hoặc chỉnh âm lượng độc lập.

**Acceptance Scenarios**:

1. **Given** người dùng cấu hình URL video YouTube hợp lệ và kích hoạt nhạc nền, **When** trình chiếu ảnh bắt đầu chạy, **Then** âm thanh từ YouTube được phát nền mượt mà đồng bộ với buổi trình chiếu.
2. **Given** nhạc nền đang phát, **When** người dùng bấm Tạm dừng (Space / Click), **Then** nhạc nền tạm dừng; khi Tiếp tục trình chiếu, nhạc nền tiếp tục phát.
3. **Given** người dùng muốn tùy chỉnh trải nghiệm, **When** điều chỉnh thanh trượt âm lượng nhạc nền trong cài đặt, **Then** âm lượng nhạc nền thay đổi tương ứng theo thời gian thực (0% - 100%).
4. **Given** video YouTube phát hết thời lượng trong lúc slideshow vẫn đang tiếp diễn, **When** kết thúc bài nhạc, **Then** hệ thống tự động lặp lại (Loop) để duy trì trải nghiệm liền mạch.
5. **Given** người dùng nhìn thanh điều khiển nổi bên dưới, **When** bấm nút Nhạc nền (🎵), **Then** nếu nhạc đã sẵn sàng thì bật/tắt tức thì; nếu chưa nhập nhạc hoặc nguồn nhạc đang bị lỗi, hệ thống tự động mở hộp thoại Cài đặt để người dùng thiết lập.
6. **Given** người dùng đang trong hộp thoại Cài đặt, **When** nhập link nhạc và bấm nút "Nghe thử", **Then** hệ thống phát thử âm thanh kiểm tra; nếu link lỗi hoặc mất mạng, hệ thống hiển thị thông báo lỗi rõ ràng.

---

### User Story 2 - Xoay & Lật Ảnh Linh Hoạt (Priority: P1)

Là một người xem ảnh thường xuyên tải ảnh chụp từ điện thoại hoặc web bị nghiêng 90 độ hoặc đảo ngược, tôi muốn có thể nhanh chóng xoay ảnh (theo chiều kim đồng hồ / ngược chiều) và lật ảnh (lật ngang, lật dọc) ngay trên màn hình xem ảnh để bức ảnh hiển thị đúng chiều mong muốn mà không làm biến đổi hay ghi đè hỏng tệp gốc.

**Why this priority**: Giải quyết trực tiếp vấn đề phổ biến nhất của người dùng khi duyệt ảnh gia đình, ảnh chân dung/phong cảnh tải từ nhiều nguồn khác nhau.

**Independent Test**: Mở một bức ảnh bị xoay dọc, nhấn nút Xoay phải 90° (hoặc phím tắt R); bức ảnh xoay đúng 90° và tự động căn chỉnh vừa vặn khung nhìn. Nhấn nút Lật ngang (hoặc phím tắt F); ảnh lật gương ngay lập tức.

**Acceptance Scenarios**:

1. **Given** ảnh đang hiển thị trên màn hình, **When** người dùng chọn Xoay Phải 90° (hoặc bấm phím tắt), **Then** ảnh xoay theo chiều kim đồng hồ thêm 90° và tự động căn chỉnh vừa khít khung nhìn hiển thị.
2. **Given** ảnh đang hiển thị, **When** người dùng chọn Xoay Trái 90° (hoặc bấm phím tắt), **Then** ảnh xoay ngược chiều kim đồng hồ 90°.
3. **Given** ảnh đang hiển thị, **When** người dùng chọn Lật Ngang (Flip Horizontal) hoặc Lật Dọc (Flip Vertical), **Then** ảnh được biến đổi đối xứng tương ứng ngay lập tức.
4. **Given** ảnh đã được xoay hoặc lật, **When** người dùng chuyển sang ảnh tiếp theo và sau đó quay lại ảnh cũ trong cùng phiên làm việc, **Then** ảnh cũ hiển thị đúng góc xoay và lật đã chỉnh (Session Cache), không bị mất trạng thái và không làm thay đổi tệp gốc trên đĩa.

---

### User Story 3 - Lựa Chọn & Cấu Hình 5 Hiệu Ứng Chuyển Cảnh Trình Chiếu (Priority: P2)

Là một người xem ảnh muốn cá nhân hóa phong cách trình chiếu, tôi muốn có thể lựa chọn giữa ít nhất 5 hiệu ứng chuyển đổi chuyển động khác nhau trong mục Cài đặt (ví dụ: Hòa tan/Fade, Trượt trái, Trượt phải, Phóng to hòa trộn/Zoom-Fade, Cắt cảnh tức thì/None), và cấu hình này được lưu trữ bền vững cho các lần sử dụng tiếp theo.

**Why this priority**: Đa dạng hóa phong cách thị giác, cho phép người dùng tùy biến theo sở thích cá nhân (trang nhã với Fade, năng động với Slide, hoặc nhanh gọn với Instant Cut).

**Independent Test**: Mở Cài đặt, chuyển hiệu ứng sang "Trượt sang trái (Slide Left)", bấm Lưu; khi chuyển ảnh tiếp theo, ảnh mới trượt từ phải sang trái mượt mà thay vì làm mờ dần như mặc định.

**Acceptance Scenarios**:

1. **Given** người dùng mở hộp thoại Cài đặt, **When** xem danh sách hiệu ứng chuyển cảnh, **Then** danh sách hiển thị tối thiểu 5 tùy chọn trực quan:
   - 1. *Hòa tan / Mờ dần (Cross-Fade)*
   - 2. *Trượt sang trái (Slide Left)*
   - 3. *Trượt sang phải (Slide Right)*
   - 4. *Phóng to hòa trộn (Zoom Fade)*
   - 5. *Chuyển tức thì (Instant / None)*
2. **Given** người dùng chọn hiệu ứng chuyển cảnh trượt và nhấn Lưu, **When** chuyển ảnh tiến (Next / Auto), **Then** ảnh chuyển theo hướng đã chọn; **When** chuyển ảnh lùi (Prev), **Then** hướng chuyển cảnh tự động đảo ngược tương ứng (ví dụ Slide Left đảo thành Slide Right) với thời lượng chuyển động tiêu chuẩn (400ms - 500ms).
3. **Given** cấu hình hiệu ứng đã chọn, **When** người dùng khởi động lại ứng dụng, **Then** hiệu ứng đã chọn vẫn được duy trì nguyên vẹn từ cấu hình đã lưu.

---

### Edge Cases

- **Mất kết nối mạng khi phát nhạc YouTube**: Nếu kết nối mạng gián đoạn, hệ thống thông báo trạng thái nhẹ nhàng hoặc tắt tiếng an toàn, không làm treo ứng dụng hay dừng chu kỳ trình chiếu ảnh.
- **URL YouTube không hợp lệ hoặc video bị gỡ / chặn bản quyền**: Hệ thống ghi nhận lỗi nguồn phát và hiển thị trạng thái cảnh báo dễ hiểu trong Cài đặt, không làm gián đoạn trình chiếu ảnh.
- **Xoay ảnh khi đang phóng to (Zoom in)**: Khi người dùng thực hiện thao tác xoay hoặc lật, hệ thống chuẩn hóa tâm quay (Center transform) và tự động căn chỉnh lại kích thước vừa vặn trong khung nhìn để tránh ảnh bị văng ra ngoài tầm mắt.
- **Chuyển ảnh liên tục với tốc độ cao (Fast Next)**: Bộ xử lý hiệu ứng chuyển cảnh (Transition Engine) phải hủy an toàn hoạt ảnh đang dở trước khi bắt đầu hoạt ảnh mới, ngăn ngừa rò rỉ bộ nhớ hoặc xung đột đồ họa.

## Requirements *(mandatory)*

### Functional Requirements

#### A. Nhạc Nền Đa Nguồn (Background Music - BGM)
- **FR-001**: Hệ thống MUST định nghĩa một cổng trừu tượng (Interface/Port) chuẩn cho dịch vụ nhạc nền (`MusicPlayerPort` / `BgmService`), cho phép hỗ trợ nhiều bộ điều khiển nguồn phát (Music Providers) độc lập.
- **FR-002**: Hệ thống MUST hiện thực hóa bộ cung cấp nguồn phát YouTube (`YouTubeBgmProvider`) là nguồn phát đầu tiên trong danh mục nguồn phát, sẵn sàng cho việc bổ sung các bộ cung cấp khác (Spotify, Local Storage, Web Radio) trong tương lai.
- **FR-003**: Cấu hình nhạc nền trong Cài đặt MUST cho phép:
  - Bật / Tắt tính năng phát nhạc nền (`bgm_enabled: bool`).
  - Lựa chọn nguồn phát hiện hành (`bgm_source: str = "youtube"`).
  - Nhập URL hoặc Video ID YouTube (`bgm_youtube_url: str`).
  - Nút "Nghe thử" (Test Audio) để kiểm tra phát nhạc trực tiếp kèm nhãn hiển thị trạng thái kết nối hoặc thông báo lỗi nếu tải thất bại.
  - Điều chỉnh âm lượng nhạc nền (`bgm_volume: int` từ 0 đến 100).
  - Tùy chọn tự động lặp lại khi hết bài (`bgm_loop: bool = True`).
- **FR-004**: Thanh điều khiển nổi (ControlPanel) MUST tích hợp nút Bật/Tắt nhạc nền (🎵/🔇):
  - Khi đã có cấu hình nguồn nhạc hợp lệ: Bấm nút để bật/tắt nhanh âm thanh nền đồng bộ với trình chiếu.
  - Khi chưa có cấu hình hoặc nguồn phát gặp lỗi: Bấm nút sẽ tự động kích hoạt hiển thị hộp thoại Cài đặt (SettingsDialog) để người dùng cấu hình.
  - Nhạc nền MUST đồng bộ với trạng thái trình chiếu: khi Slideshow Tạm dừng (Pause), nhạc nền tạm dừng; khi Slideshow Tiếp tục (Play), nhạc nền tiếp tục phát; khi đóng ứng dụng, nhạc nền dừng hoàn toàn và giải phóng tài nguyên.

#### B. Xoay & Lật Ảnh (Image Rotation & Flipping)
- **FR-005**: Hệ thống MUST cung cấp các thao tác biến đổi hình học khung nhìn:
  - Xoay 90 độ theo chiều kim đồng hồ (Rotate Clockwise 90°).
  - Xoay 90 độ ngược chiều kim đồng hồ (Rotate Counter-Clockwise 90°).
  - Lật ảnh theo trục ngang (Flip Horizontal).
  - Lật ảnh theo trục dọc (Flip Vertical).
  - Đặt lại biến đổi về mặc định (Reset Transform).
- **FR-006**: Thao tác xoay/lật ảnh MUST được truy cập dễ dàng qua các nút bấm trên thanh công cụ điều khiển, thực đơn Tùy chọn (Option Menu) và hệ thống phím tắt trực quan (ví dụ: `R` xoay phải, `Shift+R` xoay trái, `F` lật ngang, `V` lật dọc).
- **FR-007**: Biến đổi xoay/lật MUST áp dụng ở cấp độ hiển thị đồ họa (Non-destructive View Transform), TUYỆT ĐỐI KHÔNG tự ý ghi đè làm thay đổi dữ liệu tệp tin ảnh gốc trên đĩa. Hệ thống MUST duy trì bộ nhớ đệm trong phiên (In-memory Session Transform Cache) để ghi nhớ góc xoay và trạng thái lật cho từng tệp ảnh trong suốt thời gian ứng dụng đang chạy.
- **FR-008**: Khi xoay hoặc lật, khung nhìn MUST tự động tính toán lại ma trận hiển thị để ảnh luôn vừa khít cửa sổ (`fitInView`) và giữ vững mốc giới hạn thu nhỏ tối thiểu cơ sở $1.0x$.

#### C. Đa Hiệu Ứng Chuyển Cảnh (Slide Transition Effects)
- **FR-009**: Hệ thống MUST cung cấp kiến trúc bộ xử lý hiệu ứng chuyển cảnh dạng mở rộng (`TransitionEngine` / `TransitionStrategy`), hỗ trợ cắm thêm các hiệu ứng mới trong tương lai.
- **FR-010**: Hệ thống MUST cung cấp sẵn tối thiểu 5 tùy chọn hiệu ứng chuyển cảnh:
  1. `fade`: Hòa tan / Mờ dần (Cross-Fade mượt mà).
  2. `slide_left`: Trượt ảnh mới từ phải sang trái khi duyệt tiến, tự động đảo chiều từ trái sang phải khi duyệt lùi (Prev).
  3. `slide_right`: Trượt ảnh mới từ trái sang phải khi duyệt tiến, tự động đảo chiều từ phải sang trái khi duyệt lùi (Prev).
  4. `zoom_fade`: Ảnh cũ phóng to dần kết hợp ảnh mới mờ dần hiện lên.
  5. `none`: Chuyển cảnh tức thì không có hoạt ảnh trễ.
- **FR-011**: Người dùng MUST có thể chọn hiệu ứng chuyển cảnh mong muốn trong hộp thoại Cài đặt (SettingsDialog) qua danh sách thả xuống (ComboBox).
- **FR-012**: Lựa chọn hiệu ứng chuyển cảnh và các thông số nhạc nền MUST được lưu trữ bền vững vào tệp cấu hình `settings.json` thông qua `JsonSettingsRepository`.

### Key Entities *(include if feature involves data)*

- **BgmConfig**: Cấu hình dịch vụ nhạc nền (`enabled: bool`, `source: str`, `source_target: str`, `volume: int`, `loop: bool`).
- **ImageTransformState**: Trạng thái biến đổi hiển thị của ảnh hiện thời (`rotation_degrees: int` {0, 90, 180, 270}, `flip_h: bool`, `flip_v: bool`).
- **TransitionType**: Danh mục kiểu hiệu ứng chuyển ảnh (`FADE`, `SLIDE_LEFT`, `SLIDE_RIGHT`, `ZOOM_FADE`, `NONE`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Người dùng có thể nghe nhạc nền phát từ liên kết YouTube trong khi trình chiếu ảnh với độ trễ nạp âm thanh ban đầu dưới 3 giây trên kết nối mạng thông thường.
- **SC-002**: 100% các thao tác Xoay (90°, 180°) và Lật (ngang, dọc) phản hồi tức thời (< 50ms), không làm vỡ bố cục hiển thị và không sửa đổi nội dung tệp tin gốc trên đĩa.
- **SC-003**: 100% các hiệu ứng trong số 5 hiệu ứng chuyển cảnh hoạt động ổn định ở tốc độ 60 FPS, không gây giật lag hay chồng chéo hình ảnh khi chuyển slide liên tục.
- **SC-004**: Mọi tùy chọn cấu hình mới (nhạc nền YouTube, âm lượng, hiệu ứng chuyển cảnh) được tự động lưu và khôi phục chính xác 100% giữa các phiên làm việc của người dùng.
- **SC-005**: Ứng dụng tiếp tục duy trì khả năng đóng gói PyInstaller độc lập thành một tệp thực thi Windows hoàn chỉnh không lỗi.

## Assumptions

- Tính năng phát nhạc YouTube yêu cầu thiết bị có kết nối Internet đang hoạt động; nếu không có Internet, ứng dụng vẫn xem ảnh và chuyển slide bình thường.
- Thao tác xoay/lật là biến đổi không phá hủy (non-destructive) nhằm ưu tiên bảo vệ tệp gốc theo Hiến pháp dự án.
- Thời lượng chuyển động của các hiệu ứng chuyển cảnh được thiết lập mặc định ở mức tiêu chuẩn công thái học thị giác (khoảng 400ms đến 500ms) để vừa đẹp mắt vừa không gây mỏi mắt người dùng.

