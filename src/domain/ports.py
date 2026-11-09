from typing import Protocol, List, Tuple, Optional
from src.domain.models import ViewerSettings


class ImageRepositoryPort(Protocol):
    """Giao diện trừu tượng cho thao tác tệp ảnh hệ thống."""
    def scan_images(self, folder: str, supported_extensions: tuple) -> List[str]:
        """Quét và trả về danh sách đường dẫn ảnh tuyệt đối trong thư mục."""
        ...

    def delete_image(self, path: str) -> Tuple[bool, str]:
        """Chuyển ảnh vào Recycle Bin an toàn."""
        ...


class SettingsRepositoryPort(Protocol):
    """Giao diện trừu tượng cho lưu trữ cấu hình."""
    def load_settings(self) -> ViewerSettings:
        """Tải cài đặt từ nguồn lưu trữ."""
        ...

    def save_settings(self, settings: ViewerSettings) -> None:
        """Lưu cài đặt vào nguồn lưu trữ."""
        ...


class SystemIntegrationPort(Protocol):
    """Giao diện trừu tượng tương tác với hệ điều hành Windows."""
    def register_file_associations(self, exe_path: str) -> None:
        """Đăng ký Open with trong Windows Registry."""
        ...

    def set_app_user_model_id(self, app_id: str) -> None:
        """Thiết lập AppUserModelID cho Windows Taskbar."""
        ...

    def reveal_in_explorer(self, file_path: str) -> None:
        """Mở Windows Explorer và highlight tệp."""
        ...


class MusicPlayerPort(Protocol):
    """Giao diện trừu tượng điều khiển nhạc nền."""
    def set_source(self, source_target: str) -> None:
        """Thiết lập nguồn phát nhạc (URL, đường dẫn tệp, hoặc định danh tài nguyên)."""
        ...

    def get_source(self) -> str:
        """Lấy nguồn phát nhạc hiện tại."""
        ...

    def play(self) -> None:
        """Bắt đầu hoặc tiếp tục phát nhạc."""
        ...

    def pause(self) -> None:
        """Tạm dừng phát nhạc."""
        ...

    def stop(self) -> None:
        """Dừng hoàn toàn phát nhạc."""
        ...

    def set_volume(self, volume: int) -> None:
        """Đặt âm lượng từ 0 đến 100."""
        ...

    def set_loop(self, loop: bool) -> None:
        """Bật/tắt chế độ lặp lại bài hát."""
        ...

    def is_playing(self) -> bool:
        """Kiểm tra trạng thái đang phát nhạc."""
        ...

    def set_error_callback(self, callback) -> None:
        """Đăng ký hàm xử lý khi có lỗi xảy ra."""
        ...

    def set_status_callback(self, callback) -> None:
        """Đăng ký hàm thông báo trạng thái (Đang tải, Sẵn sàng, v.v.)."""
        ...

