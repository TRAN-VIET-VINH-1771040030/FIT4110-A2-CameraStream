from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(
    title="AI Vision Service (Mock)",
    description="Mock AI Service for Camera Stream - YOLOv8 simulation",
    version="1.0.0"
)

# === Models ===
class DetectRequest(BaseModel):
    camera_id: str
    image_url: str
    timestamp: datetime
    confidence_threshold: Optional[float] = 0.5

class Detection(BaseModel):
    label: str
    confidence: float
    bbox: dict

class DetectResponse(BaseModel):
    detection_id: str
    camera_id: str
    detections: List[Detection]
    risk_level: str
    model_version: str
    processing_time_ms: int
    timestamp: datetime

# === Endpoints ===
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "ai-vision-mock",
        "version": "1.0.0",
        "modelLoaded": True,
        "modelVersion": "yolov8n-v1.0",
        "time": datetime.now().isoformat()
    }

@app.post("/predict")
async def predict(request: DetectRequest):
    # Giả lập kết quả detection
    mock_detections = [
        Detection(
            label="person",
            confidence=0.92,
            bbox={"x": 100, "y": 50, "width": 80, "height": 150}
        ),
        Detection(
            label="backpack",
            confidence=0.68,
            bbox={"x": 120, "y": 180, "width": 30, "height": 40}
        )
    ]
    
    return DetectResponse(
        detection_id=str(uuid.uuid4()),
        camera_id=request.camera_id,
        detections=mock_detections,
        risk_level="LOW",
        model_version="yolov8n-v1.0",
        processing_time_ms=45,
        timestamp=datetime.now()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)