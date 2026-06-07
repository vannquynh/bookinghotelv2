from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

SECRET_KEY = "Key_udpt"
DB_CONFIG = {"dbname": "hotel_db", "user": "postgres", "password": "dozikuto", "host": "db", "port": "5432"}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(" ")[1] if 'Authorization' in request.headers else None
        if not token: return jsonify({'message': 'Vui lòng đăng nhập!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(f"DEBUG: Token payload = {data}")
            # Hỗ trợ cả 2 định dạng token: cũ ('user') và mới ('username')
            full_name = data.get('full_name')
            role = data.get('role', 'user')
            # Truyền cả full_name và role vào hàm xử lý
            return f(full_name, role, *args, **kwargs)
        except Exception as e:
            print(f"DEBUG: Token decode error = {e}")
            return jsonify({'message': 'Token sai!'}), 401
    return decorated

@app.route('/book', methods=['POST'])
@token_required
def book_room(current_user, role):
    data = request.json
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # 1. Lấy giá phòng
        cur.execute("SELECT name, price FROM rooms WHERE id = %s FOR UPDATE", (data['room_id'],))
        room = cur.fetchone()
        if not room: return jsonify({"message": "Phòng không tồn tại"}), 404

        # 2. Tính số ngày ở
        d1 = datetime.strptime(data['check_in'], "%Y-%m-%d")
        d2 = datetime.strptime(data['check_out'], "%Y-%m-%d")
        days = (d2 - d1).days
        if days <= 0: days = 1 # Ở trong ngày tính 1 ngày
        
        total_price = room['price'] * days

        # 3. Kiểm tra trùng lịch
        cur.execute("""
            SELECT id FROM bookings 
            WHERE room_id = %s AND status NOT IN ('CANCELLED') 
            AND check_in < %s AND check_out > %s
        """, (data['room_id'], data['check_out'], data['check_in']))
        
        if cur.fetchone(): return jsonify({"status": "fail", "message": "Phòng đã có người đặt trong thời gian này!"}), 400

        # 4. Tạo đơn 
        cur.execute("""
            INSERT INTO bookings (room_id, customer_name, check_in, check_out, total_price, status) 
            VALUES (%s, %s, %s, %s, %s, 'PENDING') RETURNING id
        """, (data['room_id'], current_user, data['check_in'], data['check_out'], total_price))
        
        new_id = cur.fetchone()['id']
        conn.commit()
        return jsonify({"status": "pending", "booking_id": new_id, "amount": total_price})
    except Exception as e:
        conn.rollback(); return jsonify({"error": str(e)}), 500
    finally: cur.close(); conn.close()

@app.route('/history', methods=['GET'])
@token_required
def get_history(current_user, role):
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
   
    cur.execute("""
        SELECT b.*, r.name as room_name, b.total_price 
        FROM bookings b 
        JOIN rooms r ON b.room_id = r.id 
        WHERE b.customer_name = %s 
        ORDER BY b.id DESC
    """, (current_user,))
    history = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(history)

@app.route('/cancel/<int:booking_id>', methods=['DELETE'])
@token_required
def cancel_booking(current_user, role, booking_id): # Thêm role để đúng cấu trúc token_required
    conn = get_db_connection(); cur = conn.cursor()
    try:
        # Bảo mật: Chỉ người đặt mới được hủy đơn của mình
        cur.execute("UPDATE bookings SET status = 'CANCELLED' WHERE id = %s AND customer_name = %s", (booking_id, current_user))
        if cur.rowcount == 0:
            return jsonify({"message": "Không thể hủy đơn hàng này!"}), 403
        conn.commit()
        return jsonify({"message": "Hủy thành công"}), 200
    except Exception as e:
        conn.rollback(); return jsonify({"message": str(e)}), 500
    finally: cur.close(); conn.close()

@app.route('/admin/bookings', methods=['GET'])
@token_required
def get_all_bookings(current_user, role):
    if role != 'admin': return jsonify({'message': 'Quyền Admin yêu cầu!'}), 403
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT b.*, r.name as room_name, r.price as room_price
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            ORDER BY b.id DESC
        """)
        bookings = cur.fetchall()
        cur.close(); conn.close()
        return jsonify(bookings)
    except Exception as e:
        cur.close(); conn.close()
        return jsonify({"message": str(e)}), 500

@app.route('/admin/bookings/<int:booking_id>/status', methods=['PUT'])
@token_required
def update_booking_status(current_user, role, booking_id):
    if role != 'admin': return jsonify({'message': 'Quyền Admin yêu cầu!'}), 403
    data = request.json
    new_status = data.get('status')
    if not new_status: return jsonify({'message': 'Thiếu trạng thái mới!'}), 400

    conn = get_db_connection(); cur = conn.cursor()
    try:
        cur.execute("UPDATE bookings SET status = %s WHERE id = %s", (new_status, booking_id))
        if cur.rowcount == 0:
            return jsonify({"message": "Không tìm thấy đơn hàng!"}), 404
        conn.commit()
        return jsonify({"message": "Cập nhật trạng thái thành công!"}), 200
    except Exception as e:
        conn.rollback(); return jsonify({"message": str(e)}), 500
    finally: cur.close(); conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4005, debug=True)