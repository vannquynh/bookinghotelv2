import pika
import time
import json
import sys
import os

# --- HÀM XỬ LÝ KHI CÓ TIN NHẮN ĐẾN ---
def callback(ch, method, properties, body):
    message = body.decode()
    try:
        data = json.loads(message)
        
        # TRƯỜNG HỢP 1: Tin nhắn từ Auth Service
        if 'event' in data:
            event_type = data.get('event')
            user = data.get('user')
            print(f" [🔐 LOG AUTH] User: {user} | Hành động: {event_type}")

        # TRƯỜNG HỢP 2: Tin nhắn từ Booking Service
        elif 'room_id' in data or 'room' in data:
            customer = data.get('customer_name', data.get('customer', 'Khách hàng'))
            room_name = data.get('room', '???')
            booking_id = data.get('booking_id', '???')
            
            print(f" [🏨 BOOKING] Nhận đơn đặt phòng #{booking_id}")
            print(f"    -> Khách: {customer} | Phòng: {room_name}")
            
            # Giả lập gửi mail (Xử lý bất đồng bộ thực thụ)
            print(f"    ⏳ Đang gửi email xác nhận...")
            time.sleep(2) 
            print(f"    ✅ [EMAIL SENT] Đã gửi tới {customer}!")

        else:
            print(f" [?] Tin nhắn lạ: {data}")

    except json.JSONDecodeError:
        print(f" [x] Lỗi format tin nhắn: {message}")
    
    # XÁC NHẬN ĐÃ XỬ LÝ XONG (Tránh mất tin nhắn nếu worker sập giữa chừng)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("-" * 50)

def start_worker():
    # Lấy host từ môi trường Docker hoặc mặc định là rabbitmq
    rabbit_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq') 

    while True:
        try:
            print(f' [*] Đang kết nối tới RabbitMQ tại: {rabbit_host}...')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
            channel = connection.channel()

            channel.queue_declare(queue='auth_logs', durable=True)
            channel.queue_declare(queue='hotel_notifications', durable=True)

            # Giới hạn mỗi lần chỉ xử lý 1 tin nhắn (Tránh quá tải worker)
            channel.basic_qos(prefetch_count=1)

            # Tắt auto_ack để đảm bảo an toàn dữ liệu
            channel.basic_consume(queue='auth_logs', on_message_callback=callback)
            channel.basic_consume(queue='hotel_notifications', on_message_callback=callback)

            print(' [*] ✅ Worker đã sẵn sàng! Đang lắng nghe...')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("❌ Không thể kết nối RabbitMQ! Thử lại sau 5s...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("🛑 Dừng Worker.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            time.sleep(5)

if __name__ == '__main__':
    start_worker()