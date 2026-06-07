-- Đảm bảo bảng bookings có cột total_amount và status đủ dài
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(12, 2),
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id),
    customer_name VARCHAR(100),
    check_in DATE,
    check_out DATE,
    total_amount NUMERIC(12, 2) DEFAULT 0, -- Cột này phải có sẵn
    status VARCHAR(20) DEFAULT 'PENDING'   -- Độ dài phải là 20
);