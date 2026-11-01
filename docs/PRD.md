# MapFlow AI — Phase A

Hệ thống quản lý **kho mô phỏng**, không kết nối kho thật. Dữ liệu mẫu sau này
phải được đánh dấu là mô phỏng ở fixtures, database và giao diện.

## Phạm vi được duyệt

| Hạng mục | Tỷ trọng | Mốc triển khai |
| --- | --- | --- |
| Foundation | 6% | M1, M2 |
| Auth và RBAC | 4% | M3 |
| Product Catalog | 7% | M4 |
| Bản đồ kho 2D | 8% | M5 |
| Đơn và dòng hàng | 5% | M6 |

M7 kiểm tra khả năng chạy từ máy sạch và ghi nhận phạm vi đã hoàn thành.
Từng milestone phải được xác nhận trước khi triển khai milestone kế tiếp.

## Người sử dụng

- Admin: quản lý users, catalog, kho/map và đơn.
- Warehouse Manager: đọc catalog/map, CRUD đơn.
- Warehouse Operator: đọc/tìm catalog, đọc map và đơn.

Role được lưu trong PostgreSQL; API không tin role gửi từ client.
Firebase Authentication xác thực ID token. M3 bổ sung DEV_AUTH cho local
và hướng dẫn Firebase Auth Emulator tùy chọn.

## Nền tảng cố định

React, TypeScript, Vite, TanStack Query, React Router; SVG cho map.
Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2, PostgreSQL.
pytest/vitest và ruff/ESLint. GitHub Actions chạy lint, test và build.
Contract OpenAPI được sửa trước API; web dùng type sinh từ contract đã commit.

## Tiêu chí cuối Phase A

Ba role đăng nhập được và có kiểm thử API 401/403; Admin CRUD SKU/ảnh/alias;
tìm không dấu ra SKU vít 50mm; xem map cùng zone/aisle/bin/level và đồ thị
nhất quán; CRUD đơn/dòng hàng, chuyển trạng thái hợp lệ và ghi audit.
Compose và seed chạy từ máy sạch, CI xanh.

## Ngoài phạm vi

Không làm Gemini/ADK/Agent, tồn theo lô, số dư tồn, reservation, movement,
thuật toán đường đi, OR-Tools, xe nâng, picking wave/task, QR, Document AI,
FCM hay analytics. Không tạo bảng hoặc endpoint dự phòng cho các phần này.
Ngoại lệ: M2 tạo/seed map_nodes và map_edges để hiển thị, không tính đường đi.

## Trạng thái tài liệu

M1 chỉ dựng foundation. Schema/seed ở M2; auth ở M3; catalog/map/orders
ở M4–M6. ERD, mô tả dữ liệu kho và báo cáo hackathon được viết đúng mốc,
không ghi nhận tính năng chưa triển khai là đã hoàn thành.
