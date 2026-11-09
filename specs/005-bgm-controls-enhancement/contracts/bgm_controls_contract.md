# Interface & UI Contracts: Nâng Cấp Điều Khiển Nhạc Nền

**Feature**: `005-bgm-controls-enhancement`
**Status**: Completed

## 1. Presenter & Application Layer Contract

Presenter cung cấp các phương thức điều khiển âm lượng thời gian thực và đồng bộ cấu hình:

```python
class ViewerPresenter:
    def set_bgm_volume(self, volume: int, persist: bool = False) -> None:
        """
        Cập nhật âm lượng thời gian thực cho trình phát nhạc.
        - volume: Giá trị 0 đến 100.
        - persist: Nếu True, lưu ngay vào settings_repo; nếu False, chỉ cập nhật runtime và bộ đệm bộ nhớ.
        """
        ...

    def persist_bgm_volume(self, volume: int) -> None:
        """
        Ghi nhận và lưu bền vững mức âm lượng mới vào settings.json.
        """
        ...
```

---

## 2. Presentation Layer: QuickVolumePopup Contract

Lớp giao diện popup hiển thị nổi điều chỉnh âm lượng nhanh:

```python
class QuickVolumePopup(QWidget):
    """
    Cửa sổ popup nổi không viền (Frameless Popup) hiển thị thanh trượt âm lượng.
    """
    volume_changed = pyqtSignal(int)      # Phát ra khi con trượt di chuyển (real-time)
    volume_released = pyqtSignal(int)     # Phát ra khi người dùng thả con trỏ chuột

    def __init__(self, parent: Optional[QWidget] = None): ...
    
    def set_volume(self, volume: int) -> None:
        """Đồng bộ giá trị ban đầu vào slider mà không kích hoạt tín hiệu."""
        ...

    def show_above(self, target_widget: QWidget) -> None:
        """
        Tính toán tọa độ toàn cục để hiển thị popup ngay phía trên target_widget.
        """
        ...
```

---

## 3. Presentation Layer: ControlPanel Contract

Mở rộng `ControlPanel` để xử lý sự kiện chuột phải và nhãn BGM trực quan:

```python
class ControlPanel(QFrame):
    bgm_volume_changed = pyqtSignal(int)      # Tín hiệu thay đổi âm lượng tức thời
    bgm_volume_saved = pyqtSignal(int)        # Tín hiệu xác nhận lưu âm lượng mới

    def set_bgm_state(self, is_enabled: bool, is_playing: bool = False) -> None:
        """
        Cập nhật tiêu đề và tooltip của nút BGM:
        - Nếu is_playing == True: text = '🔇 Tắt nhạc', tooltip = 'Tắt nhạc nền (Chuột phải để chỉnh âm lượng)'
        - Nếu is_playing == False: text = '🎵 Bật nhạc', tooltip = 'Bật nhạc nền (Chuột phải để chỉnh âm lượng)'
        """
        ...
```

---

## 4. Presentation Layer: SettingsDialog Contract

Quy định hành vi của ComboBox nguồn phát và slider âm lượng:

- `self.slider_bgm_volume.valueChanged`: Kết nối trực tiếp với `self.presenter.set_bgm_volume(val)`.
- `self.cmb_bgm_source`:
  - Mục `"youtube"`: `item.setEnabled(True)`.
  - Mục `"local"`, `"spotify"`: `item.setEnabled(False)`.

