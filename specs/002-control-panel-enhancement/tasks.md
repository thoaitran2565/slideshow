# Tasks: Nâng Cao Độ Rõ Nét & Ghi Nhớ Trạng Thái Thanh Điều Khiển

**Input**: Design documents from `specs/002-control-panel-enhancement/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)

**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/`

**Organization**: Các tác vụ được phân bổ tuần tự theo các tầng Clean Architecture và ánh xạ tới từng User Story để đảm bảo tính độc lập và khả năng kiểm thử liên tục.

## Format: `[TaskID] [P?] [Story?] Description with file path`

- **[P]**: Có thể chạy song song (các tệp độc lập, không phụ thuộc nhau)
- **[Story]**: Gắn nhãn User Story (`[US1]`, `[US2]`, `[US3]`)
- Mô tả tác vụ luôn chỉ định đường dẫn tệp cụ thể và trích dẫn ràng buộc xác thực rõ ràng

---

## Phase 1: Foundational (Mở Rộng Domain Entity & Infrastructure Persistence)

**Purpose**: Bổ sung các trường dữ liệu và phương thức lưu trữ nền tảng chặn trước các User Story

- [X] T001 [P] Mở rộng thực thể `ViewerSettings` trong `src/domain/models.py` với `is_random: bool = False` và `show_control_panel: bool = True` (ràng buộc: boolean thuần túy, có giá trị mặc định)
- [X] T002 [P] Cập nhật `JsonSettingsRepository` trong `src/infrastructure/json_settings_repo.py` để đọc và ghi `is_random` và `show_control_panel` từ `settings.json` kèm fallback mặc định an toàn
- [X] T003 Cập nhật `ManageSettingsUseCase` trong `src/application/use_cases.py` bổ sung phương thức `update_random_state()` và `update_panel_visibility()`

**Checkpoint**: Tầng Domain, Infrastructure và Application đã sẵn sàng hỗ trợ lưu trữ trạng thái mới.

---

## Phase 2: User Story 1 (P1) - Hiển Thị Rõ Nét Thanh Điều Khiển Trên Mọi Nền Ảnh Sáng (High Contrast & Drop Shadow)

**Goal**: Đảm bảo thanh điều khiển và nút hiện công cụ luôn nổi bật, sắc nét 100% trên các bức ảnh nền trắng hoặc quá sáng

- [X] T004 [P] [US1] Nâng cấp QSS của `ControlPanel` trong `src/presentation/views/control_panel.py` với nền tối đặc `#121212` (95%), viền sáng sắc nét (`border: 2px solid rgba(255, 255, 255, 120)`) và các nút chức năng có nền xám đen đậm (`rgba(35, 35, 35, 230)`)
- [X] T005 [P] [US1] Tích hợp hiệu ứng đổ bóng nổi `QGraphicsDropShadowEffect` (màu đen `rgba(0, 0, 0, 210)`, blur radius 24px, y-offset 4px) vào `ControlPanel` trong `src/presentation/views/control_panel.py`
- [X] T006 [US1] Nâng cấp nút "👁️ Hiện thanh công cụ" (`btn_show_panel`) trong `src/presentation/views/viewer_window.py` với viền sáng rõ nét và hiệu ứng đổ bóng `QGraphicsDropShadowEffect` để nổi bật trên nền ảnh trắng

**Checkpoint**: Thanh điều khiển và nút hiện công cụ hiển thị rõ ràng, không bị chìm trên ảnh nền trắng.

---

## Phase 3: User Story 2 (P1) - Ghi Nhớ Trạng Thái Chế Độ Phát Ngẫu Nhiên (Random Mode Persistence)

**Goal**: Tự động lưu và khôi phục chế độ phát ngẫu nhiên (Random) qua các phiên làm việc của người dùng

- [X] T007 [P] [US2] Mở rộng `ViewerPresenter` trong `src/presentation/presenter.py` để tự động lưu trạng thái `is_random` vào cấu hình mỗi khi người dùng gọi `set_random()`
- [X] T008 [US2] Cập nhật khởi tạo `PhotoViewerWindow` trong `src/presentation/views/viewer_window.py` để khôi phục trạng thái `is_random` đã lưu từ cấu hình (kích hoạt `btn_random.setChecked`, đồng bộ nhãn `🔀 Random - <tên file>` và danh sách `Playlist`)

**Checkpoint**: Bật nút Random, tắt app và mở lại, ứng dụng tiếp tục phát ngẫu nhiên mà không cần bấm lại nút.

---

## Phase 4: User Story 3 (P2) - Ghi Nhớ Trạng Thái Ẩn/Hiện Thanh Điều Khiển (Visibility Persistence)

**Goal**: Tự động lưu và khôi phục trạng thái ẩn hoặc hiện của thanh công cụ qua các phiên làm việc

- [X] T009 [P] [US3] Mở rộng `ViewerPresenter` trong `src/presentation/presenter.py` bổ sung phương thức `set_control_panel_visibility()` để ghi nhận trạng thái hiển thị của thanh công cụ vào cấu hình
- [X] T010 [US3] Cập nhật phương thức `toggle_control_panel()` trong `src/presentation/views/viewer_window.py` để tự động gọi Presenter lưu trạng thái `show_control_panel` khi người dùng bấm nút Ẩn/Hiện hoặc phím tắt `H`
- [X] T011 [US3] Cập nhật khởi tạo `PhotoViewerWindow` trong `src/presentation/views/viewer_window.py` để tự động khôi phục trạng thái ẩn hoặc hiện của thanh công cụ từ `presenter.settings.show_control_panel` khi mở ứng dụng

**Checkpoint**: Ẩn thanh công cụ, tắt app và mở lại, thanh công cụ vẫn ẩn sẵn và nút "Hiện thanh công cụ" hiển thị sẵn sàng.

---

## Phase 5: Polish & Xác Thực Toàn Diện

**Purpose**: Kiểm thử end-to-end các kịch bản thực tế và xác nhận tính toàn vẹn của ứng dụng

- [X] T012 Chạy kiểm thử xác thực 3 kịch bản theo hướng dẫn tại `specs/002-control-panel-enhancement/quickstart.md`
- [X] T013 Xác nhận tính tương thích đóng gói PyInstaller với `slideshow.spec`

---

## Dependencies & Execution Order

### Phase Dependencies
1. **Phase 1 (Foundational)**: Có thể bắt đầu ngay lập tức; chặn các pha ghi nhớ trạng thái.
2. **Phase 2 (User Story 1 - UI High Contrast)**: Có thể làm song song hoặc độc lập với Phase 1.
3. **Phase 3 (User Story 2 - Random Persistence)**: Phụ thuộc vào Phase 1.
4. **Phase 4 (User Story 3 - Visibility Persistence)**: Phụ thuộc vào Phase 1.
5. **Phase 5 (Polish & Validation)**: Thực thi cuối cùng sau khi hoàn tất các pha trước.

### Parallel Opportunities
- T001, T002 có thể triển khai song song trong Phase 1.
- T004, T005 có thể triển khai song song trong Phase 2.
- T007, T009 có thể triển khai song song trong tầng Presenter.
