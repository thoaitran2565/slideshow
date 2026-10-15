# Hướng Dẫn Cài Đặt, Chạy Và Đóng Gói Ứng Dụng Trình Chiếu Ảnh

Tài liệu này hướng dẫn từng bước cách thiết lập môi trường, chạy mã nguồn, sử dụng phần mềm và đóng gói thành file thực thi `.exe` trên Windows bằng **VS Code**.

---

## 1. Cấu Trúc Thư Mục Dự Án

Đảm bảo thư mục dự án của bạn có cấu trúc như sau:

```text
PhotoViewerApp/
├── images/             <-- Chứa các file ảnh (.jpg, .png, .webp,...)
│   ├── sample1.jpg
│   └── sample2.png
├── main.py             <-- File mã nguồn chính
└── README.md           <-- File hướng dẫn này
```

---

## 2. Cài Đặt Thư Viện Cần Thiết

Mở **Terminal** trong VS Code (`Ctrl + ~`) hoặc `Command Prompt` / `PowerShell` tại thư mục dự án và thực hiện các lệnh sau:

### Bước 2.1: Cài đặt các thư viện bổ trợ cho ứng dụng
```bash
pip install PyQt6 send2trash
```

* **`PyQt6`**: Thư viện đồ họa tạo giao diện ứng dụng.
* **`send2trash`**: Thư viện hỗ trợ xóa ảnh an toàn vào Thùng rác Windows.

### Bước 2.2: Cài đặt công cụ đóng gói file .exe
```bash
python -m pip install pyinstaller
```

---

## 3. Cách Chạy Ứng Dụng Từ Mã Nguồn (VS Code)

1. Copy tất cả các ảnh bạn muốn trình chiếu vào thư mục `images/`.
2. Mở file `main.py` trong VS Code.
3. Chạy lệnh sau trong Terminal để bắt đầu trình chiếu:
   ```bash
   python main.py
   ```

---

## 4. Cách Đóng Gói Thành File `.exe` Chạy Độc Lập

Đóng gói ứng dụng giúp bạn có thể chạy phần mềm trên bất kỳ máy tính Windows nào mà **không cần cài đặt Python**.

### Bước 4.1: Chạy lệnh đóng gói
Trong Terminal của VS Code, chạy lệnh:
```bash
python -m PyInstaller --noconsole --onefile main.py
python -m PyInstaller --noconsole --onefile --name Slideshow --icon=app_icon.ico main.py
```

* `--noconsole`: Ẩn màn hình đen CMD khi ứng dụng khởi chạy.
* `--onefile`: Đóng gói tất cả thành 1 file `.exe` duy nhất.

### Bước 4.2: Vị trí file sau khi build
Sau khi PyInstaller hoàn tất, file thực thi sẽ được tạo ra tại:
```text
PhotoViewerApp/
└── dist/
    └── main.exe       <-- File chạy ứng dụng
```

### Bước 4.3: Cách sử dụng file `.exe`
1. Copy file `main.exe` trong thư mục `dist` ra thư mục bạn muốn đặt ứng dụng.
2. Tạo hoặc copy thư mục `images` chứa ảnh nằm **cùng cấp** với file `main.exe`.
3. Nhấp đôi chuột vào `main.exe` để khởi chạy phần mềm.

---

## 5. Hướng Dẫn Sử Dụng & Phím Tắt

### Thao tác bằng chuột
* **Double Click (Nhấp đôi chuột)**: Bật / Tắt chế độ Fullscreen (Toàn màn hình).
* **Cuộn chuột (Mouse Wheel)**: Ph phóng to / Thu nhỏ ảnh.
* **Kéo giữ chuột (Drag & Drop)**: Di chuyển vị trí ảnh khi đang zoom.

### Bàn phím & Phím tắt
* **`Mũi tên Trái (◄)`**: Quay lại ảnh trước (Prev).
* **`Mũi tên Phải (►)`**: Chuyển sang ảnh tiếp theo (Next).
* **`Phím Cách (Spacebar)`**: Dừng / Tiếp tục trình chiếu tự động (Pause/Play).
* **`F11`**: Bật / Tắt chế độ Fullscreen.
* **`Esc`**: Thoát khỏi chế độ Fullscreen.

### Bảng điều khiển (Control Panel)
* **◄ Prev / Next ►**: Chuyển ảnh thủ công mà không ảnh hưởng đến bộ đếm thời gian tự động.
* **🎨 Background**: Chọn màu nền tùy thích cho phần khung hình bị thừa khi tỷ lệ ảnh không lấp đầy màn hình.
* **⚙ Options**: 
  * *Copy Tệp Ảnh*: Copy đường dẫn file.
  * *Mở Trong Thư Mục*: Mở Windows Explorer và chọn trực tiếp file ảnh hiện tại.
  * *Xoay Phải 90°*: Xoay ảnh đang xem.
  * *Xóa Ảnh*: Đưa ảnh hiện tại vào Thùng rác an toàn.


## Đăng Ký "Open With" Với Windows (Mở Ảnh Trực Tiếp)

Để có thể bấm chuột phải vào bất kỳ file ảnh nào trên máy tính $\rightarrow$ chọn **Open with** $\rightarrow$ chọn ứng dụng của bạn để mở và trình chiếu ngay lập tức, hãy làm theo các bước sau:

1. Đảm bảo file `Slideshow.exe` của bạn nằm đúng tại đường dẫn: 
   `D:\Code\apps\slideshow_app\dist\Slideshow.exe` *(nếu đường dẫn của bạn khác, hãy mở file `.reg` ở bước 2 và sửa lại cho khớp với thực tế)*.
2. Tạo một file văn bản mới ngoài thư mục dự án và đặt tên là **`setup_assoc.reg`** với nội dung sau:
   ```text
   Windows Registry Editor Version 5.00

   [HKEY_CURRENT_USER\Software\Classes\.jpg]
   @="SlideshowApp.Image"

   [HKEY_CURRENT_USER\Software\Classes\.jpeg]
   @="SlideshowApp.Image"

   [HKEY_CURRENT_USER\Software\Classes\.png]
   @="SlideshowApp.Image"

   [HKEY_CURRENT_USER\Software\Classes\.bmp]
   @="SlideshowApp.Image"

   [HKEY_CURRENT_USER\Software\Classes\.webp]
   @="SlideshowApp.Image"

   [HKEY_CURRENT_USER\Software\Classes\SlideshowApp.Image]
   @="Trình Chiếu Ảnh Cá Nhân"

   [HKEY_CURRENT_USER\Software\Classes\SlideshowApp.Image\shell\open\command]
   @="\"D:\\Code\\apps\\slideshow_app\\dist\\Slideshow.exe\" \"%1\""

Bấm đúp chuột vào file setup_assoc.reg vừa tạo $\rightarrow$ chọn Yes / Continue để Windows thêm thông tin vào Registry.Từ bây giờ, bạn có thể nhấp chuột phải vào file ảnh bất kỳ, chọn Open with để phần mềm mở lên và trình chiếu chính bức ảnh đó!
Test open with file: python main.py "C:\Users\TenUser\Pictures\anh_test.jpg"