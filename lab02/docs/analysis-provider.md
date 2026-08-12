# Analysis - Camera Stream (Provider)

**Service:** Camera Stream Service
**Vai trò:** Provider (cung cấp API cho AI Vision)
**Product:** A
**Ngày:** 2026-05-02

---

## 1. Service Overview

### 1.1 Mô tả
Camera Stream Service nhận dữ liệu từ camera, quản lý frame ảnh/video stream, và gọi AI Vision khi phát hiện điều kiện cần phân tích.

### 1.2 Vai trò trong hệ thống
- **Provider cho:** AI Vision Service (cung cấp API để AI Vision gọi)
- **Consumer của:** AI Vision Service (nhận kết quả phân tích)
- **Consumer của:** Camera hardware (nhận frame ảnh)

### 1.3 Service Boundary
