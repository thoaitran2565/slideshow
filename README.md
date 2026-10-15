# 🖼️ PhotoViewerApp — Ứng Dụng Trình Chiếu Ảnh

Ứng dụng trình chiếu ảnh trên Windows, được xây dựng bằng **Python** và **PyQt6**. Tài liệu này hướng dẫn cài đặt môi trường, chạy ứng dụng, đóng gói thành tệp `.exe` và đăng ký mở ảnh bằng Windows.

---

## 📚 Mục lục

- [✨ Tính năng](#-tính-năng)
- [📁 Cấu trúc dự án](#-cấu-trúc-dự-án)
- [⚙️ Yêu cầu](#️-yêu-cầu)
- [🚀 Cài đặt và chạy](#-cài-đặt-và-chạy)
- [📦 Đóng gói thành EXE](#-đóng-gói-thành-exe)
- [🎮 Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [🪟 Đăng ký Open with trên Windows](#-đăng-ký-open-with-trên-windows)
- [🛠️ Khắc phục sự cố](#️-khắc-phục-sự-cố)

## ✨ Tính năng

- Trình chiếu ảnh và chuyển ảnh trước/sau.
- Phóng to, thu nhỏ và kéo ảnh khi đang zoom.
- Chuyển đổi chế độ toàn màn hình.
- Tạm dừng hoặc tiếp tục trình chiếu tự động.
- Tùy chỉnh màu nền hiển thị.
- Sao chép đường dẫn, mở vị trí tệp ảnh và xoay ảnh 90° sang phải.
- Đưa ảnh vào Thùng rác Windows bằng `send2trash`.
- Đóng gói ứng dụng thành tệp thực thi `.exe`.

## 📁 Cấu trúc dự án

```text
PhotoViewerApp/
├── images/             # Thư mục chứa ảnh trình chiếu
│   ├── sample1.jpg
│   └── sample2.png
├── main.py             # Mã nguồn chính
├── app_icon.ico        # Biểu tượng ứng dụng (tùy chọn khi build)
└── README.md           # Tài liệu hướng dẫn
```

> **Lưu ý:** Kiểm tra mã nguồn để xác nhận ứng dụng đọc ảnh từ `images/` hay từ đường dẫn được truyền vào khi khởi chạy.

## ⚙️ Yêu cầu

- Windows
- Python đã cài đặt và có thể gọi bằng lệnh `python`
- Visual Studio Code (khuyến nghị)
- Kết nối Internet khi cài thư viện

## 🚀 Cài đặt và chạy

### 1. Mở dự án

Mở thư mục `PhotoViewerApp/` bằng VS Code, sau đó mở Terminal bằng **Ctrl + `**.

### 2. Cài đặt thư viện

Chạy các lệnh sau trong Terminal:

```bash
python -m pip install PyQt6 send2trash
python -m pip install pyinstaller
```

| Thư viện | Vai trò |
|---|---|
| `PyQt6` | Xây dựng giao diện đồ họa |
| `send2trash` | Đưa tệp vào Thùng rác thay vì xóa vĩnh viễn |
| `PyInstaller` | Đóng gói chương trình Python thành tệp thực thi |

### 3. Chạy ứng dụng từ mã nguồn

```bash
python main.py
```

Nếu mã nguồn hỗ trợ tham số đường dẫn ảnh, bạn có thể chạy theo mẫu:

```bash
python main.py "C:\Users\TenUser\Pictures\anh_test.jpg"
```

Thay đường dẫn ví dụ bằng đường dẫn ảnh thực tế trên máy tính.

## 📦 Đóng gói thành EXE

Mở Terminal tại thư mục chứa `main.py`.

### Cách 1: Đóng gói với tên mặc định

```bash
python -m PyInstaller --noconsole --onefile main.py
```

### Cách 2: Đóng gói thành `Slideshow.exe` kèm biểu tượng

Đặt tệp `app_icon.ico` cạnh `main.py`, sau đó chạy:

```bash
python -m PyInstaller --noconsole --onefile --name Slideshow --icon=app_icon.ico main.py
```

**Ý nghĩa tham số:**

| Tham số | Ý nghĩa |
|---|---|
| `--noconsole` | Không hiện cửa sổ console khi khởi chạy ứng dụng GUI |
| `--onefile` | Đóng gói thành một tệp thực thi duy nhất |
| `--name Slideshow` | Đặt tên tệp đầu ra là `Slideshow.exe` |
| `--icon=app_icon.ico` | Đặt biểu tượng cho tệp EXE |

Sau khi build thành công, tệp thường nằm tại:

```text
PhotoViewerApp/
├── build/
├── dist/
│   └── Slideshow.exe
└── Slideshow.spec
```

### Chạy ứng dụng đã đóng gói

1. Mở thư mục `dist/`.
2. Chạy `Slideshow.exe`.
3. Nếu ứng dụng cần thư mục ảnh đi kèm, hãy đặt thư mục đó đúng vị trí mà mã nguồn mong đợi.

> **Lưu ý:** `--onefile` đóng gói chương trình và các thư viện phụ thuộc vào một EXE, nhưng không tự động bảo đảm các ảnh bên ngoài hoặc tài nguyên tùy chỉnh được đóng gói. Hãy kiểm tra ứng dụng trên máy đích trước khi phân phối.

## 🎮 Hướng dẫn sử dụng

### Thao tác bằng chuột

| Thao tác | Chức năng |
|---|---|
| Nhấp đúp chuột | Bật/tắt chế độ toàn màn hình |
| Cuộn con lăn | Phóng to/thu nhỏ ảnh |
| Giữ và kéo chuột | Di chuyển ảnh khi đang phóng to |

### Phím tắt

| Phím | Chức năng |
|---|---|
| `←` | Xem ảnh trước |
| `→` | Xem ảnh tiếp theo |
| `Space` | Tạm dừng/tiếp tục trình chiếu tự động |
| `F11` | Bật/tắt toàn màn hình |
| `Esc` | Thoát chế độ toàn màn hình |

### Bảng điều khiển

- **Prev / Next:** chuyển ảnh thủ công.
- **Background:** thay đổi màu nền khu vực không được ảnh lấp đầy.
- **Options:**
  - **Copy Tệp Ảnh:** sao chép đường dẫn tệp ảnh.
  - **Mở Trong Thư Mục:** mở File Explorer và chọn ảnh hiện tại.
  - **Xoay Phải 90°:** xoay ảnh đang xem.
  - **Xóa Ảnh:** đưa ảnh vào Thùng rác Windows.

Tên nút và hành vi thực tế có thể khác tùy phiên bản mã nguồn.

## 🪟 Đăng ký “Open with” trên Windows

Thiết lập này giúp Windows hiển thị ứng dụng trong danh sách **Open with (Mở bằng)** cho các định dạng ảnh được đăng ký.

> **Cảnh báo:** Tệp `.reg` chỉnh sửa Windows Registry. Chỉ chạy tệp bạn đã kiểm tra. Đường dẫn EXE phải khớp với vị trí thực tế trên máy.

### 1. Xác định đường dẫn EXE

Ví dụ:

```text
D:\Code\apps\slideshow_app\dist\Slideshow.exe
```

Nếu EXE nằm ở vị trí khác, hãy thay đường dẫn trong nội dung bên dưới.

### 2. Tạo tệp `setup_assoc.reg`

Mở Notepad, dán nội dung sau và sửa đường dẫn EXE nếu cần:

```reg
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\Applications\Slideshow.exe\shell\open\command]
@="\"D:\\Code\\apps\\slideshow_app\\dist\\Slideshow.exe\" \"%1\""

[HKEY_CURRENT_USER\Software\Classes\.jpg\OpenWithList\Slideshow.exe]

[HKEY_CURRENT_USER\Software\Classes\.jpeg\OpenWithList\Slideshow.exe]

[HKEY_CURRENT_USER\Software\Classes\.png\OpenWithList\Slideshow.exe]

[HKEY_CURRENT_USER\Software\Classes\.bmp\OpenWithList\Slideshow.exe]

[HKEY_CURRENT_USER\Software\Classes\.webp\OpenWithList\Slideshow.exe]
```

Lưu tệp với tên **`setup_assoc.reg`**. Trong hộp thoại Save As, chọn **Save as type: All Files** để tránh bị lưu thành `setup_assoc.reg.txt`.

### 3. Thêm đăng ký vào Windows

1. Nhấp đúp `setup_assoc.reg`.
2. Kiểm tra thông báo, sau đó xác nhận để thêm thông tin vào Registry.
3. Nhấp chuột phải vào tệp ảnh → **Open with** → chọn `Slideshow.exe`.

Nếu ứng dụng không mở đúng ảnh được chọn, hãy xác nhận `main.py` có xử lý tham số đường dẫn ảnh (`%1`) hay không. Việc đăng ký “Open with” không tự bổ sung khả năng này vào mã nguồn.

## 🛠️ Khắc phục sự cố

- **Không nhận diện lệnh `python`:** cài Python và bật tùy chọn thêm Python vào `PATH`, sau đó mở lại Terminal.
- **Thiếu thư viện:** chạy lại `python -m pip install PyQt6 send2trash`.
- **Không tạo được EXE:** kiểm tra lỗi trong Terminal và xác nhận PyInstaller đã cài bằng `python -m pip show pyinstaller`.
- **EXE không có biểu tượng:** kiểm tra tệp `app_icon.ico` tồn tại và dùng lệnh build có `--icon=app_icon.ico`.
- **Mở ảnh bằng tham số không hoạt động:** kiểm tra mã nguồn có đọc đối số dòng lệnh hay không.
- **EXE không tìm thấy ảnh:** kiểm tra vị trí thư mục ảnh và cách ứng dụng xác định thư mục làm việc.

---

## 📄 Giấy phép

Tài liệu nguồn chưa nêu giấy phép của dự án. Nếu dự định công khai hoặc phân phối dự án, hãy bổ sung giấy phép phù hợp.

---

<p align="center">
  <i>PhotoViewerApp — đơn giản hóa trải nghiệm trình chiếu ảnh trên Windows.</i>
</p>
