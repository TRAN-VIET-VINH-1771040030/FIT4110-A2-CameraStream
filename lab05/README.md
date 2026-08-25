# Lab 05 - Docker Compose & Readiness Check

**Camera Stream Service** - Điều phối đa dịch vụ với Docker Compose

---

## 📌 Mục tiêu

- Định nghĩa và chạy nhiều service với Docker Compose
- Kết nối API, Database (PostgreSQL), AI Service (mock)
- Sử dụng healthcheck và `depends_on` để đảm bảo thứ tự khởi động
- Service discovery qua tên service (DNS nội bộ)

---

## 🏗️ Cấu trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose Stack                     │
│                                                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │   Database   │   │  AI Service  │   │     API      │      │
│  │ (PostgreSQL) │   │    (Mock)    │   │  (FastAPI)   │      │
│  │  port: 5432  │   │  port: 9000  │   │  port: 8001  │      │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                             │                                 │
│                    team-internal network                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Cấu trúc thư mục

```
lab05/
├── docker-compose.yml         # Định nghĩa multi-container
├── Dockerfile                 # Build API service
├── Dockerfile.ai              # Build AI service
├── Makefile                   # Lệnh nhanh
├── .env.example                # Biến môi trường mẫu
├── RUN_COMPOSE.md              # Hướng dẫn chạy
├── README.md                   # Tài liệu lab05
├── src/
│   ├── camera_app/
│   │   └── main.py             # Camera Stream API
│   └── ai_service/
│       ├── main.py             # AI Vision Mock
│       └── requirements.txt
├── checklists/
│   └── readiness-checklist.md  # Checklist readiness
├── postman/
│   ├── collections/
│   └── environments/
└── reports/
    └── newman-lab05-compose.json
```

---

## 🚀 Cách chạy

### 1. Clone repository

```bash
git clone https://github.com/TRAN-VIET-VINH-1771040030/FIT4110-A2-CameraStream.git
cd FIT4110-A2-CameraStream/lab05
```

### 2. Tạo file .env

```bash
cp .env.example .env
```

### 3. Chạy Docker Compose

```bash
docker compose up -d --build
```

### 4. Kiểm tra các service

```bash
# Kiểm tra API
curl http://localhost:8001/health

# Kiểm tra AI Service
curl http://localhost:9000/health

# Kiểm tra container
docker compose ps
```

### 5. Chạy Newman test

```bash
npx newman run postman/collections/CameraStream.postman_collection.json \
  -e postman/environments/CameraStream_local.postman_environment.json \
  -r cli,json --reporter-json-export reports/newman-lab05-compose.json
```

### 6. Dừng stack

```bash
docker compose down
```

---

## 📊 Kết quả

| Service | Trạng thái | Port |
|---|---|---|
| Database | ✅ Healthy | (internal) |
| AI Service | ✅ Healthy | 9000 |
| API | ✅ Healthy | 8001 |

**Newman test:** ✅ 4/4 PASS

---

## 📋 Service Discovery

Trong Docker Compose, các service gọi nhau bằng tên service:

| Từ | Gọi | URL |
|---|---|---|
| API | Database | `db:5432` |
| API | AI Service | `ai-service:9000` |
| Host | API | `http://localhost:8001` |

---

## 📤 Commit

```bash
git add lab05/
git commit -m "lab05: complete docker compose with newman test pass"
git push origin main
```

**Ngày hoàn thành:** 2026-08-25
**Team:** Camera Stream