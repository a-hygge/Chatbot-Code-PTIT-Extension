# Chatbot Code PTIT Extension

Tiện ích mở rộng (extension) hỗ trợ hướng dẫn nghiệp vụ cho người dùng trang Code PTIT. Extension này tích hợp chatbot thông minh trả lời các câu hỏi về nghiệp vụ sử dụng Code PTIT, hỗ trợ giảng viên và người quản trị hệ thống.

## Tính năng chính

- **Chatbot tích hợp**: Cung cấp hướng dẫn nghiệp vụ ngay trên trang Code PTIT
- **Phân loại câu hỏi thông minh**: Tự động phân loại câu hỏi theo nhiều loại nhiệm vụ khác nhau
- **Gợi ý video hướng dẫn**: Cung cấp links đến các video hướng dẫn liên quan
- **Giao diện thân thiện**: Giao diện đơn giản, dễ sử dụng, tích hợp trực tiếp vào trang Code PTIT

## Cài đặt

### Yêu cầu hệ thống

- Python 3.8+
- Google Chrome hoặc trình duyệt tương thích với Chrome Extensions
- Kết nối Internet

### Cài đặt backend (server)

1. Clone repository này về máy của bạn
2. Cài đặt các thư viện cần thiết:

   ```bash
   pip install -r requirements.txt
   ```
3. Tạo file `.env` trong thư mục gốc với nội dung sau:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
4. Khởi động server:

   ```bash
   python server.py
   ```

### Cài đặt extension cho Chrome

1. Mở Chrome và truy cập `chrome://extensions/`
2. Bật "Developer mode" ở góc phải trên cùng
3. Chọn "Load unpacked" và chọn thư mục `extension` từ repository
4. Extension đã sẵn sàng để sử dụng trên trang Code PTIT

## Cấu trúc dự án

- `chatbot.py` - Core logic cho chatbot và xử lý câu hỏi
- `server.py` - API server để xử lý các yêu cầu từ extension
- `link.py` - Quản lý links và kết nối đến video hướng dẫn
- `playlist_videos.json` - Dữ liệu video hướng dẫn
- `extension/` - Mã nguồn cho Chrome Extension
  - `manifest.json` - Cấu hình extension
  - `injector.js` - Chèn chatbot vào trang Code PTIT
  - `background.js` - Xử lý các sự kiện nền
  - `style.css` - Định dạng giao diện chatbot
- `logs/` - Chứa logs từ server

## Sử dụng

1. Truy cập trang [Code PTIT](https://code.ptit.edu.vn)
2. Chatbot sẽ tự động hiển thị trên trang
3. Đặt câu hỏi về nghiệp vụ và nhận câu trả lời cùng các video liên quan

## Phát triển

### Thêm video hướng dẫn mới

1. Thêm thông tin video mới vào file `playlist_videos.json` theo định dạng:

   ```json
   {
     "title": "Tiêu đề video",
     "url": "URL đến video YouTube",
     "category": "Loại nhiệm vụ"
   }
   ```

### Chỉnh sửa mô hình phân loại

Chỉnh sửa hàm `classify_task()` trong `chatbot.py` để thêm hoặc sửa các loại nhiệm vụ.