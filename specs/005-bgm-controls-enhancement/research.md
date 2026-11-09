# Research: Nâng Cấp Điều Khiển Nhạc Nền (Live Volume, Quick Popup, BGM Label & Source Protection)

**Feature**: `005-bgm-controls-enhancement`
**Status**: Completed

## 1. Cơ Chế Điều Chỉnh Âm Lượng Thời Gian Thực (Live Volume Binding)

### Vấn Đề
Trước đây, trong `SettingsDialog`, sự kiện `slider_bgm_volume.valueChanged` chỉ cập nhật nhãn văn bản `lbl_bgm_vol_val` mà không phát tín hiệu thay đổi âm lượng tức thời xuống `manage_bgm_uc.set_volume(val)`. Do đó, khi người dùng đang bấm "Nghe thử", âm thanh phát ra không đổi cho đến khi bấm dừng rồi phát lại.

### Quyết Định
- Kết nối `self.slider_bgm_volume.valueChanged` trực tiếp với hàm xử lý thời gian thực:
  ```python
  def _on_volume_slider_changed(self, val: int):
      self.lbl_bgm_vol_val.setText(f"{val}%")
      if self.presenter and self.presenter.manage_bgm_uc:
          self.presenter.manage_bgm_uc.set_volume(val)
  ```
- Trong `QtMusicPlayer`, thuộc tính `self.audio_output.setVolume(volume / 100.0)` nhận giá trị float từ 0.0 đến 1.0 và áp dụng tức thời lên stream âm thanh đang phát (hỗ trợ native bởi `PyQt6.QtMultimedia.QAudioOutput`).
- Áp dụng kỹ thuật tách biệt: `valueChanged` cập nhật bộ đệm âm thanh của phần cứng, sự kiện `sliderReleased` (hoặc khi lưu dialog) cập nhật `settings.json` để tối ưu hóa I/O đĩa.

### Giải Pháp Thay Thế Đã Xem Xét
- *Chỉ lưu khi bấm "Lưu Cài Đặt" mà không đổi âm thanh khi nghe thử*: Bị loại bỏ vì người dùng không cảm nhận được mức âm lượng vừa nghe, gây trải nghiệm gián đoạn.

---

## 2. Popup Chỉnh Âm Lượng Nhanh Bằng Chuột Phải Trên Nút BGM

### Vấn Đề
Người dùng muốn nhấp chuột phải vào nút BGM ở thanh công cụ dưới đáy (`ControlPanel`) để mở thanh trượt âm lượng nhanh và kéo chỉnh trực tiếp âm thanh bài nhạc đang phát mà không cần mở hộp thoại Cài đặt.

### Quyết Định
- Cấu hình nút `btn_bgm` trong `ControlPanel`:
  ```python
  self.btn_bgm.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
  self.btn_bgm.customContextMenuRequested.connect(self._show_volume_popup)
  ```
- Xây dựng lớp giao diện `QuickVolumePopup(QWidget)` với cờ `Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint`:
  - Nền mờ bán trong suốt Dark Theme `#1e1e1e` viền `#00adb5`, bo tròn góc hiện đại.
  - Chứa biểu tượng loa `🔊`, thanh trượt ngang `QSlider(Qt.Orientation.Horizontal)` từ 0 đến 100, và nhãn phần trăm.
  - Vị trí hiển thị: Tự động tính toán tọa độ toàn cục (`mapToGlobal`) xuất hiện ngay phía trên nút `btn_bgm`.
  - Kết nối tín hiệu `volume_changed(int)` tới `presenter.set_bgm_volume(val)` cập nhật âm lượng ngay lập tức trong luồng nhạc đang phát.
  - Tự động đóng khi người dùng nhấp chuột ra ngoài (hành vi chuẩn của `Qt.WindowType.Popup`).

### Giải Pháp Thay Thế Đã Xem Xét
- *Sử dụng QMenu thông thường*: `QMenu` có thể nhúng widget qua `QWidgetAction`, tuy nhiên việc tùy biến CSS kích thước và căn chỉnh thanh trượt trên `QMenu` phức tạp hơn và dễ bị style mặc định của hệ điều hành can thiệp. Lớp `QWidget(..., Qt.WindowType.Popup)` mang lại sự tự do thiết kế UI Dark Theme đồng bộ 100% với ứng dụng.

---

## 3. Chuẩn Hóa Nhãn & Kích Thước Nút BGM Trên Thanh Điều Khiển

### Vấn Đề
Nút BGM trước đây hiển thị `"🎵 Nhạc"` hoặc `"🔇 Nhạc"`, chưa thể hiện rõ hành động của nút là "Bật nhạc" hay "Tắt nhạc".

### Quyết Định
- Cập nhật phương thức `set_bgm_state(self, is_enabled: bool, is_playing: bool)`:
  - Khi nhạc đang tắt (`not is_playing`): Hiển thị text `"🎵 Bật nhạc"`, tooltip `"Bật nhạc nền (Chuột phải để chỉnh âm lượng)"`.
  - Khi nhạc đang bật (`is_playing`): Hiển thị text `"🔇 Tắt nhạc"`, tooltip `"Tắt nhạc nền (Chuột phải để chỉnh âm lượng)"`.
- Do văn bản dài hơn trước ("Bật nhạc" / "Tắt nhạc" thay vì "Nhạc"), điều chỉnh kích thước thanh `ControlPanel` trong `viewer_window.py` từ `panel_width = 720` lên `panel_width = 760` và tăng min-width nút để đảm bảo bố cục không bị co ép khi hiển thị trên mọi độ phân giải màn hình.

---

## 4. Vô Hiệu Hóa Lựa Chọn Nguồn Nhạc Chưa Khả Dụng Trong QComboBox

### Vấn Đề
Trong danh sách nguồn phát nhạc của `SettingsDialog`, có các mục "Spotify" và "Tệp ổ cứng cục bộ" chưa được phát triển. Nếu người dùng chọn vào có thể gây hiểu nhầm hoặc lỗi logic.

### Quyết Định
- Trong `SettingsDialog`, nạp các tùy chọn kèm nhãn trực quan:
  ```python
  self.cmb_bgm_source.addItem("YouTube (Trực tuyến)", "youtube")
  self.cmb_bgm_source.addItem("Tệp ổ cứng cục bộ (Sắp ra mắt)", "local")
  self.cmb_bgm_source.addItem("Spotify (Sắp ra mắt)", "spotify")
  ```
- Sử dụng `QStandardItemModel` để vô hiệu hóa (disable) các mục chưa hỗ trợ:
  ```python
  model = self.cmb_bgm_source.model()
  for i in range(self.cmb_bgm_source.count()):
      data = self.cmb_bgm_source.itemData(i)
      if data != "youtube":
          item = model.item(i)
          if item:
              item.setEnabled(False)
  ```
- Nhờ cơ chế này, người dùng vẫn thấy danh mục lộ trình mở rộng của ứng dụng nhưng không thể click chọn các nguồn chưa phát triển.

