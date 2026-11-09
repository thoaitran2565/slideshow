# Feature Specification: Giới Hạn Mức Thu Nhỏ Tối Thiểu (Chỉ Cho Phép Phóng To Chi Tiết)

**Feature Branch**: `003-restrict-min-zoom`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "Tính năng cuộn chuột để phóng to thu nhỏ thì chỉ cho phóng to thôi và không cho thu nhỏ hơn kích thước gốc, tại mặt định khi ảnh được hiển thị thì nó đã hiện lên full ảnh rồi nên chỉ cần cho phóng to thôi"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ngăn Chặn Thu Nhỏ Dưới Kích Thước Vừa Khung Nhìn (Priority: P1)

Là một người xem ảnh, khi một bức ảnh được nạp lên màn hình ở trạng thái vừa khít cửa sổ (Fit in View), nếu tôi vô tình hoặc cố ý cuộn con lăn chuột xuống (Zoom out), tôi muốn ứng dụng giữ nguyên kích thước đầy đủ của bức ảnh và không cho phép thu nhỏ thêm, để bức ảnh không bị thu nhỏ thành một chấm li ti lọt thỏm giữa màn hình gây khó chịu.

**Why this priority**: Loại bỏ trải nghiệm khó chịu khi người dùng lỡ cuộn chuột làm ảnh bị co nhỏ hơn bình thường; bảo đảm ảnh luôn hiển thị tối đa diện tích khả dụng.

**Independent Test**: Mở bất kỳ ảnh nào, thực hiện cuộn chuột xuống liên tục; xác nhận kích thước ảnh không đổi và giữ nguyên trạng thái vừa khít màn hình ban đầu.

**Acceptance Scenarios**:

1. **Given** ảnh đang hiển thị ở kích thước ban đầu (Fit in View), **When** người dùng cuộn con lăn chuột xuống (Zoom out), **Then** ứng dụng giữ nguyên tỷ lệ kích thước ban đầu, không thu nhỏ ảnh dưới mức này.
2. **Given** ảnh đang ở kích thước ban đầu, **When** người dùng thực hiện kéo chuột (Pan), **Then** ảnh không bị trôi lệch khỏi vị trí trung tâm.

---

### User Story 2 - Phóng To Chi Tiết & Thu Nhỏ Mượt Mà Về Kích Thước Gốc (Priority: P1)

Là một người xem ảnh muốn soi chi tiết (văn bản, chi tiết khuôn mặt, cảnh quan), tôi muốn cuộn chuột lên để phóng to ảnh tùy ý, và sau đó có thể cuộn chuột xuống để thu nhỏ lại dần dần cho tới khi chạm ngưỡng kích thước ban đầu thì dừng lại hoàn hảo và căn giữa ngay ngắn.

**Why this priority**: Đảm bảo chức năng zoom vẫn đáp ứng trọn vẹn nhu cầu soi chi tiết mà không làm mất đi khả năng quay về góc nhìn tổng thể một cách dễ dàng.

**Independent Test**: Cuộn chuột lên 3 lần để phóng to ảnh, sau đó cuộn chuột xuống 5 lần; xác nhận ảnh thu nhỏ lại và dừng đúng ở kích thước ban đầu (Fit in View) mà không bị thu nhỏ quá đà.

**Acceptance Scenarios**:

1. **Given** ảnh đang ở kích thước ban đầu, **When** người dùng cuộn chuột lên (Zoom in), **Then** ảnh phóng to dần mượt mà theo từng nấc cuộn và cho phép kéo rê (Pan) để xem các góc của ảnh.
2. **Given** ảnh đang được phóng to (mức zoom > 1.0x), **When** người dùng cuộn chuột xuống (Zoom out), **Then** ảnh thu nhỏ dần lại; khi chạm ngưỡng kích thước ban đầu, ứng dụng tự động khóa lại ở mức Fit in View và căn giữa khung hình.

---

### User Story 3 - Tự Động Đặt Lại Tỷ Lệ Chuẩn Khi Đổi Ảnh Hoặc Đổi Cửa Sổ (Priority: P2)

Là một người dùng trình chiếu ảnh liên tục, tôi muốn mỗi khi ứng dụng chuyển sang ảnh mới (tự động hoặc bấm Next/Prev) hoặc khi tôi thay đổi kích thước cửa sổ (Resize / Fullscreen), ảnh mới luôn tự động hiển thị vừa khít khung nhìn với mốc giới hạn thu nhỏ được đặt lại tương ứng.

**Why this priority**: Đảm bảo tính nhất quán qua từng bức ảnh có tỷ lệ khung hình khác nhau (ảnh dọc, ảnh ngang, ảnh panorama).

**Independent Test**: Đang zoom to bức ảnh hiện tại, bấm phím mũi tên Phải để chuyển sang ảnh tiếp theo; xác nhận ảnh mới hiển thị vừa khít khung nhìn ở mức 1.0x ban đầu.

**Acceptance Scenarios**:

1. **Given** bức ảnh hiện tại đang ở trạng thái zoom to, **When** ứng dụng chuyển sang ảnh tiếp theo (thủ công hoặc tự động), **Then** ảnh mới được nạp ở trạng thái vừa khít cửa sổ (Fit in View) và mốc giới hạn thu nhỏ được khởi tạo lại cho ảnh mới.
2. **Given** cửa sổ ứng dụng được phóng to, thu nhỏ hoặc chuyển sang Fullscreen, **When** sự kiện resize xảy ra, **Then** khung nhìn được căn chỉnh lại và mốc giới hạn thu nhỏ được tính toán lại theo kích thước mới của viewport.

---

### Edge Cases

- **Ảnh có kích thước phân giải rất nhỏ (ví dụ 100x100px)**: Ứng dụng hiển thị vừa khung nhìn theo tỷ lệ giữ nguyên khung hình (`KeepAspectRatio`), và mốc giới hạn thu nhỏ tối thiểu vẫn là kích thước vừa vặn ban đầu đó.
- **Cuộn chuột cực nhanh xuống dưới (Fast scroll down)**: Thuật toán kẹp giá trị (Clamp) phải chặn ngay lập tức, không để bước nhảy scale rơi xuống dưới ngưỡng 1.0x của view ban đầu.
- **Chuyển đổi giữa chế độ Toàn màn hình (Fullscreen) và Cửa sổ thường (Normal Window)**: Hệ thống phải tự động tính toán lại ma trận biến đổi (Transformation Matrix) để ngưỡng chặn kích thước gốc luôn chính xác theo độ phân giải màn hình hiện thời.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Khung nhìn hiển thị ảnh `QGraphicsView` MUST duy trì một hệ số phóng đại tương đối (`current_zoom_level` hoặc tỷ lệ ma trận biến đổi so với trạng thái `fitInView`), với giá trị cơ sở tại kích thước vừa vặn ban đầu là $1.0$.
- **FR-002**: Khi người dùng thực hiện thao tác cuộn chuột lên (`angleDelta().y() > 0`), hệ thống MUST cho phép phóng to ảnh theo hệ số phóng đại (ví dụ bước nhảy $1.15$), có thể phóng to tới một ngưỡng tối đa an toàn (ví dụ tối đa $20.0x$).
- **FR-003**: Khi người dùng thực hiện thao tác cuộn chuột xuống (`angleDelta().y() < 0`), hệ thống MUST kiểm tra mức zoom hiện tại:
  - Nếu mức zoom hiện tại lớn hơn $1.0$, cho phép thu nhỏ dần.
  - Nếu bước thu nhỏ tiếp theo khiến mức zoom $\le 1.0$, hệ thống MUST kẹp (clamp) mức zoom về đúng $1.0$ và gọi lệnh đưa ảnh về trạng thái vừa khít ban đầu (`fitInView`) kèm căn giữa hoàn hảo.
  - Nếu mức zoom hiện tại đã là $1.0$ (hoặc nhỏ hơn), hệ thống MUST bỏ qua sự kiện thu nhỏ (ignore/no-op), TUYỆT ĐỐI KHÔNG thu nhỏ ảnh nhỏ hơn kích thước vừa vặn ban đầu.
- **FR-004**: Khi nạp ảnh mới (`show_image()`) hoặc khi kích thước cửa sổ thay đổi (`resizeEvent()`), hệ thống MUST tự động reset hệ số zoom về $1.0$ và gọi `fitInView` để đảm bảo mốc kích thước gốc luôn đồng bộ với kích thước khung nhìn hiện tại.
- **FR-005**: Thao tác kéo rê ảnh (Pan bằng `ScrollHandDrag`) chỉ có hiệu lực khi mức zoom $> 1.0$; khi ảnh ở mức zoom cơ sở $1.0$, ảnh giữ nguyên vị trí căn giữa màn hình.
- **FR-006**: Tất cả logic kiểm soát tỷ lệ zoom MUST được đóng gói gọn gàng trong tầng Presentation (`PhotoViewerWindow`), không làm ảnh hưởng tới kiến trúc Clean Architecture hay các tầng Use Cases/Domain.

### Key Entities

- **ZoomState**: Trạng thái kiểm soát mức zoom hiển thị trong cửa sổ trình chiếu (`base_scale`, `current_zoom_factor: float`, với min clamp = $1.0$, max clamp = $20.0$).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% các thao tác cuộn chuột xuống khi ảnh đang ở kích thước ban đầu đều không làm ảnh bị thu nhỏ thêm (mức zoom tối thiểu bị khóa cứng ở $1.0x$).
- **SC-002**: Thao tác phóng to chi tiết hoạt động mượt mà (60 FPS) và cho phép cuộn ngược về đúng $1.0x$ mà không bị lệch tâm hay méo tỷ lệ khung hình.
- **SC-003**: Khi chuyển ảnh hoặc resize cửa sổ, 100% các bức ảnh mới đều tự động hiển thị vừa khít khung nhìn ban đầu ở mức $1.0x$.
- **SC-004**: Không có bất kỳ lỗi hồi quy nào đối với các tính năng xem ảnh, trình chiếu tự động, phím tắt hoặc thanh công cụ điều khiển.

## Assumptions

- Kích thước gốc được định nghĩa là kích thước hiển thị ban đầu khi ảnh vừa vặn trong cửa sổ hiển thị (`fitInView` với `KeepAspectRatio`), thay vì kích thước pixel vật lý 1:1 của file ảnh gốc (bởi vì ảnh độ phân giải 4K nếu hiện 1:1 sẽ tràn khung, còn ảnh nhỏ sẽ bị vỡ).
- Mức phóng to tối đa được giới hạn ở $20.0x$ để tránh tràn bộ nhớ đệm đồ họa của hệ thống.

