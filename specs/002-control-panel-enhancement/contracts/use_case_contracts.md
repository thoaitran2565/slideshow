# Use Case Contracts: State Persistence

**Feature**: `002-control-panel-enhancement`  
**Date**: 2026-11-09  
**Status**: Draft  

---

## 1. Mở Rộng `ManageSettingsUseCase`

```python
class ManageSettingsUseCase:
    ...
    def update_random_state(self, is_random: bool) -> None:
        """Cập nhật trạng thái phát ngẫu nhiên vào settings.json."""
        settings = self.settings_repo.load_settings()
        settings.is_random = is_random
        self.settings_repo.save_settings(settings)

    def update_panel_visibility(self, show_panel: bool) -> None:
        """Cập nhật trạng thái hiển thị của thanh điều khiển vào settings.json."""
        settings = self.settings_repo.load_settings()
        settings.show_control_panel = show_panel
        self.settings_repo.save_settings(settings)
```

---

## 2. Mở Rộng `ViewerPresenter`

```python
class ViewerPresenter:
    ...
    def set_random(self, is_random: bool) -> None:
        """Kích hoạt hoặc tắt ngẫu nhiên trong Playlist và tự động lưu cấu hình."""
        self.navigate_uc.set_random(self.playlist, is_random)
        self.manage_settings_uc.update_random_state(is_random)
        self.settings.is_random = is_random

    def set_control_panel_visibility(self, show_panel: bool) -> None:
        """Lưu trạng thái hiển thị của thanh công cụ vào cấu hình."""
        self.manage_settings_uc.update_panel_visibility(show_panel)
        self.settings.show_control_panel = show_panel
```

