import sys
from PyQt6.QtWidgets import QApplication
from src.viewer_window import PhotoViewerWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PhotoViewerWindow(image_dir="images")
    viewer.show()
    sys.exit(app.exec())