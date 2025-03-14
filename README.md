# Flask Blog

## Giới thiệu
Đây là một dự án blog đơn giản được xây dựng bằng Flask, hỗ trợ hiển thị bài viết với hình ảnh và trang dashboard.

## Cấu trúc dự án
```
ptud-gk-de-1/
│── app.py               # File chính chạy ứng dụng Flask
│── templates/
│   ├── base.html        # Template cơ bản
│   ├── index.html       # Trang chính hiển thị bài viết (Single Column)
│   ├── dashboard.html   # Trang dashboard
│── static/
│   ├── styles.css       # File CSS
│── models.py            # (Dự phòng nếu cần thêm database)
│── requirements.txt     # Danh sách thư viện cần cài đặt
│── README.md            # Hướng dẫn cài đặt
```

## Hướng dẫn cài đặt
### 1. Clone dự án
```sh
git clone https://github.com/yourusername/ptud-gk-de-1.git
cd ptud-gk-de-1
```

### 2. Cài đặt môi trường ảo (tuỳ chọn)
```sh
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate     # Trên Windows
```

### 3. Cài đặt các thư viện cần thiết
```sh
pip install -r requirements.txt
```

### 4. Chạy ứng dụng
```sh
python app.py
```

Sau đó, mở trình duyệt và truy cập **`http://127.0.0.1:5000/`** để xem trang web.

## Tính năng chính
- Hiển thị danh sách bài viết theo bố cục **Single Column (Một Cột)**
- Hiển thị trang dashboard thống kê số lượng bài viết
- Thêm bài viết 
- Xóa bài viết

## Thông tin tác giả
- **Tên:** [Hồ Minh Luân]
- **Mã sinh viên:** [22644751]
## Tài khoản admin
- Tên: admin
- Mật khẩu: admin123