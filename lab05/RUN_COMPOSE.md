# RUN_COMPOSE - Camera Stream Service

## Yêu cầu

- Docker Desktop
- Git

## Các bước chạy

### 1. Clone repository

```bash
git clone https://github.com/TRAN-VIET-VINH-1771040030/FIT4110-A2-CameraStream.git
cd FIT4110-A2-CameraStream/lab05
```

### 2. Chạy Docker Compose

```bash
docker compose up -d --build
```

### 3. Kiểm tra

```bash
docker compose ps
curl http://localhost:8001/health
```

### 4. Test motion detection

```bash
curl -X POST http://localhost:8001/frames/process -H "Content-Type: application/json" -d "{}"
```

### 5. Dừng stack

```bash
docker compose down
```