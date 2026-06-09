DỰ ÁN: HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN CALESTIA HOTEL
I. TỔNG QUAN DỰ ÁN
1.1 Giới thiệu
Hệ thống đặt phòng khách sạn Calestia Hotel là một ứng dụng web cho phép khách hàng đặt phòng trực tuyến, quản lý đặt phòng, và thanh toán đa dạng. Hệ thống được xây dựng theo kiến trúc microservices với giao diện hiện đại, thân thiện người dùng.

1.2 Mục tiêu dự án
Cung cấp nền tảng đặt phòng trực tuyến tiện lợi
Đa dạng hóa phương thức thanh toán
Quản lý đặt phòng hiệu quả cho admin
Tối ưu hóa trải nghiệm người dùng với giao diện hiện đại
II. KIẾN TRÚC HỆ THỐNG
2.1 Kiến trúc Microservices
Hệ thống được chia thành các services độc lập:

Auth Service (Port 4001): Xác thực người dùng, đăng ký, đăng nhập
Room Service (Port 4002): Quản lý thông tin phòng
Booking Service (Port 4005): Xử lý đặt phòng, lịch sử đặt phòng
Payment Service (Port 4003): Xử lý thanh toán đa dạng
Worker Service: Xử lý gửi email thông báo
Web Server (Nginx): Gateway, serve static files, reverse proxy
2.2 Công nghệ sử dụng
Backend:

Python Flask (Web framework)
PostgreSQL (Database)
RabbitMQ (Message Queue)
JWT (Authentication)
Docker (Containerization)
Frontend:

HTML5, CSS3, JavaScript
Bootstrap 5 (CSS framework)
Google Fonts (Poppins)
Nginx (Web server)
DevOps:

Docker Compose
Nginx (Reverse Proxy)
III. CÁC TÍNH NĂNG CHÍNH
3.1 Tính năng dành cho khách hàng
3.1.1 Đăng ký & Đăng nhập
Đăng ký tài khoản mới với username, password, full name
Đăng nhập với JWT token
Phân quyền user/admin
3.1.2 Xem danh sách phòng
Hiển thị danh sách phòng với hình ảnh
Hiển thị giá phòng
Click vào phòng để xem chi tiết trong modal
Hiển thị mô tả chi tiết từng hạng phòng:
Phòng Standard: 25m², tiện nghi cơ bản
Phòng Deluxe: 35m², view thành phố
Phòng VIP: 45m², view biển/vườn, bồn tắm jacuzzi
Phòng Tổng Thống: 80m², view toàn cảnh
3.1.3 Đặt phòng
Click vào phòng để xem chi tiết và chọn dịch vụ bổ sung
Chọn dịch vụ bổ sung với giá:
🥐 Breakfast Included – 150.000 VND
🚗 Airport Transfer – 300.000 VND
🛏️ Extra Bed – 120.000 VND
⏰ Early Check-in – 200.000 VND
⏰ Late Check-out – 200.000 VND
🍽️ Room Service – 100.000 VND
🏊 Swimming Pool – 100.000 VND
💪 Gym/Fitness Center – 100.000 VND
Chọn ngày nhận/trả phòng
Chọn phương thức thanh toán đa dạng:
Thanh toán toàn bộ (100%) - Trạng thái: PAID
Đặt cọc giữ chỗ (30%) - Trạng thái: DEPOSIT_PAID
Tiền mặt (tại quầy) - Trạng thái: PENDING_CASH
Chuyển khoản ngân hàng - Trạng thái: PENDING_TRANSFER (có mã QR)
Thẻ tín dụng/Ghi nợ - Trạng thái: PAID/DEPOSIT_PAID
Xác nhận đặt phòng với thông báo phù hợp
Tổng thanh toán bao gồm giá phòng và dịch vụ bổ sung
3.1.4 Lịch sử đặt phòng
Xem lịch sử đặt phòng cá nhân
Hiển thị trạng thái đơn hàng với màu sắc:
Chờ thanh toán (vàng)
Đã thanh toán (xanh lá)
Đã đặt cọc (xanh dương)
Chờ tiền mặt (đỏ)
Chuyển khoản (xám)
Đã hủy (đỏ)
Thanh toán nốt số tiền còn lại (nếu đã đặt cọc)
Hủy đơn hàng
3.2 Tính năng dành cho Admin
3.2.1 Quản lý phòng
Thêm phòng mới với tên, giá, mô tả
Xóa phòng
Xem danh sách phòng
3.2.2 Quản lý đặt phòng
Xem tất cả đơn đặt phòng
Xác nhận đơn hàng (chuyển sang PAID)
Hủy đơn hàng
Xem thông tin chi tiết: khách hàng, phòng, ngày, giá, trạng thái
3.3 Tính năng khác
3.3.1 Liên hệ
Hotline: 1900 123 456
Email: booking@calestiahotel.com
Mạng xã hội: Facebook, Instagram, Twitter, YouTube
IV. DATABASE SCHEMA
4.1 Bảng Users
- id (integer, primary key)
- username (varchar(100))
- password (varchar(100))
- full_name (varchar(100))
- role (varchar(20), default: 'user')
4.2 Bảng Rooms
- id (integer, primary key)
- name (varchar(100))
- price (integer)
- status (varchar(20), default: 'AVAILABLE')
- image_url (varchar(255))
- description (text)
4.3 Bảng Bookings
- id (integer, primary key)
- room_id (integer)
- customer_name (varchar(100))
- check_in (date)
- check_out (date)
- total_price (integer)
- status (varchar(20), default: 'PENDING')
Các trạng thái booking:

PENDING: Chờ thanh toán
PAID: Đã thanh toán
DEPOSIT_PAID: Đã đặt cọc
PENDING_CASH: Chờ thanh toán tiền mặt
PENDING_TRANSFER: Chờ chuyển khoản
CANCELLED: Đã hủy
V. API ENDPOINTS
5.1 Auth Service (Port 4001)
POST /register - Đăng ký tài khoản
POST /login - Đăng nhập
5.2 Room Service (Port 4002)
GET /rooms - Lấy danh sách phòng
POST /rooms - Thêm phòng (Admin)
DELETE /rooms/<id> - Xóa phòng (Admin)
5.3 Booking Service (Port 4005)
POST /book - Đặt phòng
GET /history - Lịch sử đặt phòng cá nhân
DELETE /cancel/<id> - Hủy đơn hàng
GET /admin/bookings - Lấy tất cả đơn hàng (Admin)
PUT /admin/bookings/<id>/status - Cập nhật trạng thái (Admin)
5.4 Payment Service (Port 4003)
POST /pay - Xử lý thanh toán
VI. GIAO DIỆN NGƯỜI DÙNG
6.1 Thiết kế
Màu sắc chủ đạo: Hồng nhạt (#fdf2f8, #fbb6ce, #f9a8d4, #ec4899)
Font chữ: Poppins (hiện đại, dễ đọc)
Logo: CALESTIA HOTEL (gradient màu hồng #ec4899 → #f472b6 → #fb7185, font size 2.2rem, nổi bật)
Layout: Responsive, thân thiện người dùng
Modal chi tiết phòng: Hiển thị thông tin chi tiết khi click vào phòng
Truncation mô tả: Mô tả phòng hiển thị tối đa 2 dòng, click để xem đầy đủ
6.2 Các trang
Trang chủ (index.html): Danh sách phòng, footer thông tin liên hệ
Đăng nhập (login.html): Form đăng nhập
Đăng ký (register.html): Form đăng ký
Đặt phòng (booking.html): Form đặt phòng với QR code chuyển khoản
Lịch sử (history.html): Lịch sử đặt phòng cá nhân
Admin (admin.html): Quản lý phòng và đặt phòng với tab system
VII. TRIỂN KHAI
7.1 Yêu cầu hệ thống
Docker Desktop
VS Code (hoặc bất kỳ editor nào)
Trình duyệt web
7.2 Cách chạy
# 1. Chuyển đến thư mục dự án
cd d:\bookinghotelv2\bookinghotelv2

# 2. Chạy Docker Compose
docker-compose up -d

# 3. Truy cập web
http://localhost
7.3 Các ports
Web: 80
Database: 5433
RabbitMQ: 5672, 15672
Auth Service: 4001
Room Service: 4002
Booking Service: 4005
Payment Service: 4003
VIII. KẾT LUẬN
Hệ thống đặt phòng khách sạn Calestia Hotel đã được triển khai thành công với đầy đủ tính năng:

Đặt phòng trực tuyến tiện lợi
Đa dạng phương thức thanh toán
Quản lý đặt phòng hiệu quả
Giao diện hiện đại, thân thiện
Kiến trúc microservices có khả năng mở rộng
Hệ thống đáp ứng nhu cầu đặt phòng của khách hàng và quản lý của admin, mang lại trải nghiệm người dùng tốt nhất.
