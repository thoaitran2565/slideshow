import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QIcon

from src.infrastructure.path_utils import get_resource_path, get_base_dir
from src.infrastructure.json_settings_repo import JsonSettingsRepository
from src.infrastructure.local_image_repo import LocalImageRepository
from src.infrastructure.windows_system_adapter import WindowsSystemAdapter

from src.application.use_cases import (
    LoadImagesUseCase, NavigatePlaylistUseCase,
    DeleteImageUseCase, ManageFavoritesUseCase, ManageSettingsUseCase,
    ManageBgmUseCase
)
from src.infrastructure.bgm.youtube_provider import YouTubeBgmProvider
from src.infrastructure.bgm.qt_music_player import QtMusicPlayer
from src.presentation.presenter import ViewerPresenter
from src.presentation.views.viewer_window import PhotoViewerWindow
from src.presentation.views.splash_screen import CustomSplashScreen
from src.presentation.views.settings_dialog import SettingsDialog


def main():
    # 1. Khởi tạo Windows System Adapter & Thiết lập môi trường OS
    system_adapter = WindowsSystemAdapter()
    system_adapter.set_app_user_model_id("PhotoViewerApp.Slideshow.Windows.1.0")

    # Đăng ký tự động Open with vào Windows Registry
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        exe_path = os.path.abspath(sys.argv[0])
    system_adapter.register_file_associations(exe_path)

    # 2. Khởi tạo QApplication
    app = QApplication(sys.argv)

    # Đặt icon ứng dụng
    icon_path = get_resource_path("app_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # 3. Khởi tạo Dependency Injection (Clean Architecture Composition Root)
    settings_repo = JsonSettingsRepository()
    image_repo = LocalImageRepository()

    load_images_uc = LoadImagesUseCase(image_repo=image_repo)
    navigate_uc = NavigatePlaylistUseCase()
    delete_image_uc = DeleteImageUseCase(image_repo=image_repo)
    manage_favorites_uc = ManageFavoritesUseCase(settings_repo=settings_repo)
    manage_settings_uc = ManageSettingsUseCase(settings_repo=settings_repo)

    # Khởi tạo dịch vụ nhạc nền
    youtube_provider = YouTubeBgmProvider()
    music_player = QtMusicPlayer(provider=youtube_provider)
    manage_bgm_uc = ManageBgmUseCase(music_player=music_player, settings_repo=settings_repo)

    presenter = ViewerPresenter(
        load_images_uc=load_images_uc,
        navigate_uc=navigate_uc,
        delete_image_uc=delete_image_uc,
        manage_favorites_uc=manage_favorites_uc,
        manage_settings_uc=manage_settings_uc,
        system_adapter=system_adapter,
        manage_bgm_uc=manage_bgm_uc
    )

    settings = presenter.settings
    # Khởi tạo mức âm lượng BGM ban đầu theo đúng cấu hình đã lưu
    music_player.set_volume(settings.bgm_volume)

    # 4. Màn hình khởi động (Splash Screen)
    splash = CustomSplashScreen()
    saved_geometry = settings.window_geometry
    if hasattr(splash, "move_to_screen_center"):
        splash.move_to_screen_center(app, saved_geometry)

    splash.show()
    app.processEvents()

    for i in range(1, 101):
        time.sleep(0.012)
        if i == 30:
            splash.set_progress(i, "Đang nạp cấu hình hệ thống...")
        elif i == 70:
            splash.set_progress(i, "Khởi tạo danh sách tài nguyên...")
        else:
            splash.set_progress(i)
        app.processEvents()

    # 5. Xử lý tham số mở tệp từ dòng lệnh ("Open with")
    target_file = None
    initial_dir = None
    if len(sys.argv) > 1:
        arg_path = sys.argv[1]
        if os.path.exists(arg_path):
            if os.path.isfile(arg_path):
                target_file = os.path.abspath(arg_path)
                initial_dir = os.path.dirname(target_file)
            elif os.path.isdir(arg_path):
                initial_dir = os.path.abspath(arg_path)

    # 6. Kiểm tra thư mục ảnh lần đầu chạy
    folder = initial_dir or settings.image_folder
    if not folder or not os.path.exists(folder):
        splash.hide()
        dialog = SettingsDialog(presenter=presenter)
        dialog.setWindowTitle("Cấu Hình Thư Mục Lần Đầu Chạy")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)
        settings = settings_repo.load_settings()
        folder = settings.image_folder

    if folder:
        presenter.settings.image_folder = folder

    # 7. Khởi tạo và hiển thị cửa sổ chính
    window = PhotoViewerWindow(presenter=presenter, start_file=target_file)
    window.show()
    splash.finish(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
