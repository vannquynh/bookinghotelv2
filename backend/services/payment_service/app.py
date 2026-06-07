from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

SECRET_KEY = "Key_udpt"
DB_CONFIG = {"dbname": "hotel_db", "user": "postgres", "password": "dozikuto", "host": "db", "port": "5432"}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(" ")[1] if 'Authorization' in request.headers else None
        if not token: return jsonify({'message': 'Thiếu Token!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return f(data['full_name'], *args, **kwargs)
        except: return jsonify({'message': 'Xác thực thất bại!'}), 401
    return decorated

@app.route('/pay', methods=['POST'])
@token_required
def process_payment(current_user):
    data = request.json
    booking_id = data.get('booking_id')
    # Nhận thêm số tiền thực tế khách gửi từ Frontend (30% hoặc 100%)
    amount_paid = data.get('amount_paid')
    payment_method = data.get('payment_method', 'full')

    conn = psycopg2.connect(**DB_CONFIG); cur = conn.cursor()
    try:
        # Lấy tổng tiền gốc của đơn hàng để so sánh
        cur.execute("SELECT total_price FROM bookings WHERE id = %s", (booking_id,))
        row = cur.fetchone()

        if row:
            total_amount = float(row[0])
            new_status = 'PAID'
            message = ""

            # Xử lý theo hình thức thanh toán
            if payment_method == 'deposit':
                # Đặt cọc 30%
                if amount_paid and float(amount_paid) < total_amount:
                    new_status = 'DEPOSIT_PAID'
                    message = f"Cảm ơn {current_user}, bạn đã đặt cọc thành công!"
                else:
                    new_status = 'PAID'
                    message = f"Cảm ơn {current_user}, thanh toán toàn bộ thành công!"
            elif payment_method == 'cash':
                # Tiền mặt - thanh toán tại quầy
                new_status = 'PENDING_CASH'
                message = f"Cảm ơn {current_user}! Đơn hàng đã được xác nhận. Vui lòng thanh toán {total_amount.toLocaleString()} VND bằng tiền mặt tại quầy khi nhận phòng."
            elif payment_method == 'transfer':
                # Chuyển khoản
                new_status = 'PENDING_TRANSFER'
                message = f"Cảm ơn {current_user}! Vui lòng chuyển khoản {total_amount.toLocaleString()} VND vào tài khoản ngân hàng của khách sạn. Số tài khoản: 1234567890 - Ngân hàng Vietcombank - Calestia Hotel"
            elif payment_method == 'card':
                # Thẻ tín dụng/Ghi nợ
                if amount_paid and float(amount_paid) < total_amount:
                    new_status = 'DEPOSIT_PAID'
                    message = f"Cảm ơn {current_user}, thanh toán thẻ thành công!"
                else:
                    new_status = 'PAID'
                    message = f"Cảm ơn {current_user}, thanh toán thẻ thành công!"
            else:
                # Thanh toán toàn bộ mặc định
                new_status = 'PAID'
                message = f"Cảm ơn {current_user}, thanh toán toàn bộ thành công!"

            # Cập nhật trạng thái tương ứng
            cur.execute("UPDATE bookings SET status = %s WHERE id = %s", (new_status, booking_id))
            conn.commit()
            return jsonify({"status": "success", "message": message})
        else:
            return jsonify({"status": "error", "message": "Không tìm thấy đơn hàng!"}), 404

    except Exception as e:
        conn.rollback(); return jsonify({"status": "error", "message": str(e)}), 500
    finally: cur.close(); conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4003, debug=True)