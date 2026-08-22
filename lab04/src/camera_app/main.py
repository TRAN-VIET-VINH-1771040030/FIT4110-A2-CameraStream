from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(
    title="Camera Stream Service",
    description="Service nhận dữ liệu từ camera và gọi AI Vision",
    version="1.0.0"
)

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

# === Fake Data ===
fake_cameras = [
    Camera(
        camera_id="cam-gate-01",
        name="Cổng chính",
        status="active",
        location="Khu vực cổng chính",
        ip_address="192.168.1.100",
        stream_url="rtsp://192.168.1.100:554/stream"
    ),
    Camera(
        camera_id="cam-parking-01",
        name="Bãi đỗ xe",
        status="active",
        location="Khu vực bãi đỗ xe",
        ip_address="192.168.1.101",
        stream_url="rtsp://192.168.1.101:554/stream"
    )
]

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)