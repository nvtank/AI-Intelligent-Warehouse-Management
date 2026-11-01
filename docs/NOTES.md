# Ghi chú và quyết định phạm vi

- M1: chưa có schema nghiệp vụ, migration nghiệp vụ hay seed.
  Alembic được cấu hình sẵn với SQLAlchemy metadata rỗng.
- M1: chỉ có `/health`, `/health/ready` và các endpoint tài liệu FastAPI.
  Health công khai; chưa có dữ liệu nghiệp vụ cần bảo vệ.
- `/health` kiểm tra tiến trình; `/health/ready` thực hiện `SELECT 1` với
  PostgreSQL và trả 503 nếu chưa cấu hình hoặc chưa kết nối được.
- `/products/{id}/locations` chưa được triển khai. Data model được yêu cầu
  chưa có quan hệ vị trí mặc định của SKU; không suy diễn tồn kho từ bin.
  Quyết định schema được chốt tại M2.
- M1 chưa cài Firebase, storage adapter hay gói auth/upload; thực hiện ở
  các mốc tương ứng sau khi được xác nhận.
- Không thêm trạng thái đơn chưa sử dụng trong M1. Các chuyển trạng thái
  nghiệp vụ được thiết kế và kiểm tra ở M6.
- Bộ sinh TypeScript nội bộ chỉ hỗ trợ phần JSON Schema đang dùng và dừng
  bằng lỗi với cấu trúc chưa hỗ trợ. Khi contract mở rộng, phải mở rộng bộ
  sinh hoặc xin phép thêm công cụ chuyên dụng; không sinh type `any` dự phòng.
- Không triển khai bất kỳ tính năng Phase B nào.
- Ngoại lệ dependency đã được xác nhận: react-dom, uvicorn, psycopg
  (binary wheel của cùng driver) và @types/react, @types/react-dom.
  Các dependency bắc cầu do stack yêu cầu được pin trong lockfile;
  không có tích hợp telemetry, analytics hay agent ở source ứng dụng.
- Không thêm httpx/jsdom/Testing Library, plugin React, TypeScript ESLint
  parser hay pydantic-settings. Test API dùng ASGI harness với standard
  library; test web dùng vitest và renderer React có sẵn.
- ESLint kiểm tra JS sau khi TypeScript transpile, còn `tsc --noEmit`
  kiểm tra kiểu/unused ở source. Chưa có rule ESLint đặc thù TypeScript.
- Kiểm tra npm khi dựng M1: dependency runtime không có advisory;
  dependency dev còn advisory moderate từ minimatch bắc cầu của ESLint.
  Không ép override major của dependency bắc cầu. Lệnh tái kiểm tra:
  `npm audit` và `npm audit --omit=dev`.
