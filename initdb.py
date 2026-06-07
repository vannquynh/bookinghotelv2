
import sqlite3
import os


if os.path.exists("hotel.db"):
    os.remove("hotel.db")

connection = sqlite3.connect('hotel.db')
cursor = connection.cursor()

print("⏳ Đang tạo bảng dữ liệu...")

# 1. Tạo bảng USERS
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL
)
''')

# 2. Tạo bảng ROOMS
cursor.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    status TEXT DEFAULT 'AVAILABLE'
)
''')

# 3. Tạo bảng BOOKINGS (Lịch sử & Đặt phòng)
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER,
    customer_name TEXT,
    check_in TEXT,
    check_out TEXT,
    total_price INTEGER,
    status TEXT DEFAULT 'PENDING',
    FOREIGN KEY(room_id) REFERENCES rooms(id)
)
''')

# 4. Thêm dữ liệu mẫu cho Phòng
cursor.execute("INSERT INTO rooms (name, price, status) VALUES ('Phòng Deluxe View Biển', 1500000, 'AVAILABLE')")
cursor.execute("INSERT INTO rooms (name, price, status) VALUES ('Phòng Standard Giường Đôi', 800000, 'AVAILABLE')")
cursor.execute("INSERT INTO rooms (name, price, status) VALUES ('Phòng VIP Tổng Thống', 5000000, 'AVAILABLE')")
cursor.execute("INSERT INTO rooms (name, price, status) VALUES ('Phòng Family Gia Đình', 2000000, 'AVAILABLE')")

connection.commit()
connection.close()

print("✅ Đã tạo file hotel.db thành công tại thư mục gốc!")