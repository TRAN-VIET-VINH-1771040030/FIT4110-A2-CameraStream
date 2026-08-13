# Lab 02 - OpenAPI Contract-First Design

**Camera Stream Service** - Thiết kế hợp đồng API bằng OpenAPI 3.1.0

---

## 📌 Mục tiêu

- Thiết kế API Contract cho Camera Stream Service
- Viết `openapi.yaml` theo chuẩn OpenAPI 3.1.0
- Đàm phán và thống nhất hợp đồng với nhóm AI Vision
- Kiểm tra hợp đồng bằng Spectral
- Chạy Mock Server bằng Prism

---

## 📁 Cấu trúc thư mục

```
lab02/
├── openapi.yaml               # API Specification
├── negotiation-log.md         # Biên bản đàm phán
├── README.md                  # Tài liệu lab02
├── package.json                # Dependencies
├── .spectral.yaml               # Spectral rules
├── campus-spectral.yaml          # Spectral rules (full)
├── docs/
│   ├── analysis-provider.md     # Phân tích góc nhìn Provider
│   └── analysis-consumer.md     # Phân tích góc nhìn Consumer
└── evidence/
    └── buoi-02/
        └── mock-screenshots/     # Ảnh minh chứng mock server
            ├── req-01-health.png
            ├── req-02-cameras.png
            ├── req-03-camera-by-id.png
            └── req-04-upload-frame.png
```

---

## 🚀 Cách chạy

### 1. Cài đặt công cụ

```bash
npm install
```

### 2. Kiểm tra OpenAPI

```bash
spectral lint openapi.yaml
```

### 3. Chạy Mock Server

```bash
prism mock openapi.yaml --port 4010
```

### 4. Test API

```bash
# Health check
curl http://127.0.0.1:4010/health

# Lấy danh sách camera
curl http://127.0.0.1:4010/cameras

# Lấy camera theo ID
curl http://127.0.0.1:4010/cameras/cam-01

# Upload frame
curl -X POST http://127.0.0.1:4010/frames -H "Content-Type: application/json" -d '{"camera_id":"cam-01","image_url":"https://example.com/frame.jpg","timestamp":"2026-08-13T09:05:00Z"}'
```

---

## ✅ Kết quả

| Công việc | Trạng thái |
|-----------|------------|
| openapi.yaml | ✅ Hoàn thành |
| Spectral lint | ⏳ Chờ kiểm tra |
| Prism mock server | ⏳ Chờ kiểm tra |
| Negotiation log | ✅ Đã đàm phán |

**Ngày hoàn thành:** 2026-08-13