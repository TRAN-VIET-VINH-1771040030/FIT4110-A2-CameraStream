from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import cv2
import requests
import numpy as np
import os
import base64
import json
import time

app = FastAPI(
    title="Camera Stream Service",
    description="Service nhận dữ liệu từ camera và gọi AI Vision",
    version="1.0.0"
)

# === Biến môi trường ===
CAMERA_URL = os.getenv('CAMERA_URL', 'https://camera.labaiotdnu.app/video?key=matkhau_cua_ban')
AI_VISION_URL = os.getenv('AI_VISION_URL', 'http://ai-vision-team:8000')
MOTION_THRESHOLD = float(os.getenv('MOTION_THRESHOLD', '0.5'))
COOLDOWN_SECONDS = int(os.getenv('COOLDOWN_SECONDS', '5'))

# === Models ===
class Camera(BaseModel):
    camera_id: str
    name: str
    status: str
    location: Optional[str] = None
    ip_address: Optional[str] = None
    stream_url: Optional[str] = None

class FrameUpload(BaseModel):
    camera_id: str
    image_url: str
    timestamp: datetime
    motion_detected: bool = False
    metadata: Optional[dict] = None

class FrameUploadResponse(BaseModel):
    frame_id: str
    status: str
    message: Optional[str] = None
    timestamp: datetime

class MotionDetectionResponse(BaseModel):
    motion_detected: bool
    motion_score: float
    snapshot: Optional[str] = None
    ai_result: Optional[dict] = None

# === Biến trạng thái ===
fake_cameras = [
    Camera(
        camera_id="cam-gate-01",
        name="Cổng chính",
        status="active",
        location="Khu vực cổng chính",
        ip_address="192.168.1.100",
        stream_url=CAMERA_URL
    ),
    Camera(
        camera_id="cam-parking-01",
        name="Bãi đỗ xe",
        status="active",
        location="Khu vực bãi đỗ xe",
        ip_address="192.168.1.101",
        stream_url=CAMERA_URL
    )
]

prev_frame = None
last_ai_call = 0

# === Hàm xử lý camera ===
def get_frame_from_stream():
    """Đọc frame từ camera stream"""
    try:
        cap = cv2.VideoCapture(CAMERA_URL)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return frame
        else:
            print("[Camera] Failed to read frame")
            return None
    except Exception as e:
        print(f"[Camera] Error: {e}")
        return None

def detect_motion(prev_frame, current_frame, threshold=MOTION_THRESHOLD):
    """Phát hiện motion bằng frame difference"""
    if prev_frame is None:
        return False, 0.0
    
    # Chuyển sang grayscale
    gray1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    
    # Tính diff
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    motion_score = np.sum(thresh) / 255 / thresh.size
    return motion_score > threshold, round(motion_score, 3)

def process_frame_for_ai(frame):
    """Tiền xử lý frame: resize, encode thành base64"""
    # Resize về 640x480
    resized = cv2.resize(frame, (640, 480))
    
    # Encode thành JPEG
    _, buffer = cv2.imencode('.jpg', resized, [cv2.IMWRITE_JPEG_QUALITY, 75])
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

async def call_ai_vision(frame_data):
    """Gửi snapshot sang AI Vision"""
    try:
        response = requests.post(
            f"{AI_VISION_URL}/api/v1/detect",
            json=frame_data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"AI Vision error: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "AI Vision timeout"}
    except Exception as e:
        return {"error": str(e)}

# === Endpoints ===
@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái service"""
    return {
        "status": "ok",
        "service": "camera-stream-service",
        "time": datetime.now().isoformat()
    }

@app.get("/cameras")
async def get_cameras(status: Optional[str] = "all"):
    """Lấy danh sách camera"""
    if status == "all":
        return fake_cameras
    return [c for c in fake_cameras if c.status == status]

@app.get("/cameras/{camera_id}")
async def get_camera_by_id(camera_id: str):
    """Lấy thông tin camera theo ID"""
    for camera in fake_cameras:
        if camera.camera_id == camera_id:
            return camera
    raise HTTPException(status_code=404, detail="Camera not found")

@app.post("/frames")
async def upload_frame(frame: FrameUpload):
    """Upload frame ảnh từ camera"""
    frame_id = f"frame-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    return FrameUploadResponse(
        frame_id=frame_id,
        status="accepted",
        message="Frame accepted for processing",
        timestamp=datetime.now()
    )

@app.post("/frames/process")
async def process_frame_from_camera():
    """Đọc frame từ camera, phát hiện motion, gửi sang AI Vision"""
    global prev_frame, last_ai_call
    
    # 1. Đọc frame từ camera
    frame = get_frame_from_stream()
    if frame is None:
        return {
            "status": "error",
            "message": "Cannot read frame from camera",
            "camera_url": CAMERA_URL
        }
    
    # 2. Phát hiện motion
    motion_detected, motion_score = detect_motion(prev_frame, frame)
    prev_frame = frame.copy()
    
    # 3. Nếu có motion và cooldown
    current_time = time.time()
    snapshot = None
    ai_result = None
    
    if motion_detected and (current_time - last_ai_call >= COOLDOWN_SECONDS):
        # 3a. Tiền xử lý frame
        image_base64 = process_frame_for_ai(frame)
        
        # 3b. Gắn metadata
        request_data = {
            "request_id": str(uuid.uuid4()),
            "event_type": "camera.motion.triggered",
            "source_service": "team-camera",
            "camera_id": "cam-gate-01",
            "timestamp": datetime.now().isoformat(),
            "location": "Main Gate A",
            "motion_detected": True,
            "motion_score": motion_score,
            "image_format": "jpg",
            "image_base64": image_base64
        }
        
        # 3c. Gửi sang AI Vision
        ai_result = await call_ai_vision(request_data)
        last_ai_call = current_time
        
        # 3d. Log kết quả
        print(f"[Camera] Motion detected! Score: {motion_score}")
        print(f"[Camera] AI Vision result: {ai_result}")
    
    return MotionDetectionResponse(
        motion_detected=motion_detected,
        motion_score=motion_score,
        snapshot=snapshot,
        ai_result=ai_result
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)