# Service Boundary - Camera Stream Service

## Actor
- Camera IP / thiet bi camera (nguon phat sinh du lieu, co the mo phong bang anh tinh neu khong co camera that)
- AI Vision Service (nhan anh de phan tich)
- Core Business Service (nhan ket qua bat thuong da qua xu ly)
- Analytics Service (nhan du lieu camera event de thong ke)

## Responsibility
- Tiep nhan frame anh hoac video stream tu camera (hoac mo phong bang anh tinh/frame URL)
- Xac dinh dieu kien can gui anh sang AI Vision (vi du: motion_detected = true)
- Gui request chua anh/frame den AI Vision Service
- Nhan ket qua phan tich (detection) tra ve tu AI Vision
- Ghi log ket qua phan tich camera
- Cung cap du lieu camera event cho Analytics Service

## Out of scope
- Khong tu thuc hien nhan dien doi tuong/AI inference (thuoc trach nhiem AI Vision Service)
- Khong luu tru video dai han hoac xu ly toan bo luong video lien tuc (chi xu ly theo frame/event)
- Khong tu quyet dinh tao canh bao hay thong bao (thuoc trach nhiem Core Business / Notification)
- Khong kiem soat quyen truy cap camera (khong phai Access Gate Service)

## Input
- camera_id (string)
- frame_url hoac anh frame (mo phong qua URL hoac upload)
- motion_detected (boolean)
- timestamp (ISO 8601)

## Output
- Ket qua trigger gui AI Vision: object, confidence, risk_level (nhan ve tu AI Vision, forward tiep)
- Log camera event (camera_id, timestamp, trang thai xu ly)
- Camera event data cho Analytics (so luong frame xu ly, so lan trigger AI Vision)

## Provider (ai goi minh / minh nhan du lieu tu ai)
- Camera IP / thiet bi mo phong camera

## Consumer (minh goi ai)
- AI Vision Service - gui anh/frame can phan tich
- Core Business Service - chuyen ket qua bat thuong sau khi AI Vision tra ve
- Analytics Service - cung cap du lieu camera event

## API/Event du kien
- POST /camera/frame - nhan frame moi tu camera (camera_id, frame_url, motion_detected, timestamp)
- GET /camera/status/{camera_id} - kiem tra trang thai xu ly gan nhat cua mot camera
- (internal) Goi POST den AI Vision Service: /vision/analyze

## So do luong du lieu

Camera IP (hoac anh mo phong)
       |
       v
Camera Stream Service
       |
       |--> AI Vision Service --> (tra ket qua detection)
       |
       |--> Core Business Service (khi co ket qua bat thuong)
       |
       +--> Analytics Service (camera event data)
