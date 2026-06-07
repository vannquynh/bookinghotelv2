from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
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
        if not token: return jsonify({'message': 'Thiếu Token!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return f(data['full_name'], data.get('role', 'user'), *args, **kwargs)
        except: return jsonify({'message': 'Token không hợp lệ!'}), 401
    return decorated

@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM rooms ORDER BY id ASC")
    rooms = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rooms)

@app.route('/rooms', methods=['POST'])
@token_required
def add_room(current_user, role):
    if role != 'admin': return jsonify({'message': 'Quyền Admin yêu cầu!'}), 403
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    description = data.get('description', '')
    cur.execute("INSERT INTO rooms (name, price, description) VALUES (%s, %s, %s)", (data['name'], data['price'], description))
    conn.commit(); cur.close(); conn.close()
    return jsonify({'status': 'success', 'message': 'Đã thêm phòng!'})

@app.route('/rooms/<int:room_id>', methods=['DELETE'])
@token_required
def delete_room(current_user, role, room_id):
    if role != 'admin': return jsonify({'message': 'Quyền Admin yêu cầu!'}), 403
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    conn.commit(); cur.close(); conn.close()
    return jsonify({'status': 'success', 'message': 'Đã xóa phòng!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4002, debug=True)