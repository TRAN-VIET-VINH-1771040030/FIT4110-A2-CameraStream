FROM python:3.11-slim

# Cài đặt thư viện hệ thống cho OpenCV (dùng gói đúng tên trong Debian Trixie)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libxcb1 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-randr0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/camera_app/ ./src/camera_app/

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.camera_app.main:app", "--host", "0.0.0.0", "--port", "8000"]