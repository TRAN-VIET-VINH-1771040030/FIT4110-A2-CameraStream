import redis
import time
import json
import os
import requests
import psycopg2
from datetime import datetime

# Kết nối Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Kết nối DB
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'db'),
    port=os.getenv('DB_PORT', 5432),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres'),
    database=os.getenv('DB_NAME', 'postgres')
)

def process_frame(frame_data):
    try:
        ai_url = os.getenv('AI_VISION_URL', 'http://ai-vision-team:8000')
        response = requests.post(
            f"{ai_url}/vision/detect",
            json=frame_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO detections (frame_id, camera_id, result, created_at) VALUES (%s, %s, %s, %s)",
                (frame_data.get('frame_id'), frame_data.get('camera_id'), json.dumps(result), datetime.now())
            )
            conn.commit()
            cur.close()
            print(f"[Worker] Processed frame {frame_data.get('frame_id')}")
        else:
            print(f"[Worker] AI Vision error: {response.status_code}")
    except Exception as e:
        print(f"[Worker] Error: {e}")

if __name__ == "__main__":
    print("[Worker] Starting...")
    while True:
        try:
            job = redis_client.lpop('frame_queue')
            if job:
                frame_data = json.loads(job)
                process_frame(frame_data)
            else:
                time.sleep(1)
        except Exception as e:
            print(f"[Worker] Error: {e}")
            time.sleep(5)