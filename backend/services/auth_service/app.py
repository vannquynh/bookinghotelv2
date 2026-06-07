from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import pika  
import json
import jwt          # Thư viện tạo Token
import datetime     # Thư viện tính thời gian

app = Flask(__name__)
CORS(app)

SECRET_KEY = "Key_udpt" 

DB_CONFIG = {
    "dbname": "hotel_db",
    "user": "postgres",
    "password": "dozikuto",  
    "host": "db",     
    "port": "5432"
}

# --- HÀM GỬI TIN NHẮN ĐẾN RABBITMQ (PRODUCER) ---
def send_auth_log(event_type, username):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='auth_logs') 
        
        log_data = {"event": event_type, "user": username}
        channel.basic_publish(
            exchange='',
            routing_key='auth_logs',
            body=json.dumps(log_data)
        )
        connection.close()
        print(f" [x] Đã đẩy log '{event_type}' vào RabbitMQ")
    except Exception as e:
        print("❌ Lỗi RabbitMQ:", e)

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("❌ Auth Service - Lỗi kết nối DB:", e)
        return None

# --- API Đăng ký ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Lỗi kết nối Database"}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM users WHERE username = %s", (data['username'],))
        if cur.fetchone():
            return jsonify({"status": "fail", "message": "Tên đăng nhập đã tồn tại!"})

        cur.execute("INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)",
                      (data['username'], data['password'], data['full_name']))
        conn.commit()

        send_auth_log("REGISTER_SUCCESS", data['username'])

        return jsonify({"status": "success", "message": "Đăng ký thành công!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# --- API Đăng nhập (TRẢ VỀ TOKEN) ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Lỗi kết nối Database"}), 500

    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
      
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                            (data['username'], data['password']))
        user = cur.fetchone()
        print(f"DEBUG DB USER: {user}") # Thêm dòng nà
        
        if user:
            send_auth_log("LOGIN_SUCCESS", data['username'])
            
            # --- TẠO TOKEN ---
            token_payload = {
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user.get('role', 'user'),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            
            # Ký tên bằng Key_Henhung
            token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
            
            return jsonify({
                "status": "success", 
                "token": token,  
                "full_name": user['full_name'],
                "role": user.get('role', 'user') # Trả về role để frontend biết đường xử lý nếu cần
            })
        else:
            send_auth_log("LOGIN_FAILED", data['username'])
            return jsonify({"status": "fail", "message": "Sai tài khoản hoặc mật khẩu!"})
    except Exception as e:
        # Thay vì chỉ print(e), hãy trả về lỗi để Frontend thấy
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    print("🚀 Auth Service (JWT Mode + Admin Role) đang chạy trên Port 4001...")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=True)