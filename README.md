# MapFlow AI

Quản lý kho vật liệu xây dựng **mô phỏng**. Repo hiện chỉ triển khai
**M1 — Foundation** của Phase A. Chưa có schema/seed, đăng nhập, catalog,
bản đồ kho hoặc đơn hàng.

## Chạy bằng Docker

Cần Docker Engine và Docker Compose **2.20.3 trở lên**.
Chạy các lệnh tại thư mục chứa README này:

```sh
cp .env.example .env
# Sửa POSTGRES_PASSWORD trong .env; nếu chạy API trên host, cập nhật DATABASE_URL tương ứng.
docker compose up --build -d --wait
```

- Web: <http://localhost:5173>
- API docs: <http://localhost:8000/docs>
- Liveness: <http://localhost:8000/health>
- PostgreSQL readiness: <http://localhost:8000/health/ready>
- PostgreSQL trên host: `localhost:55432`.

Compose tự đợi database và API healthy trước khi chạy web. API tạo URL
database từ các biến PostgreSQL để mật khẩu chứa ký tự đặc biệt vẫn dùng được.
Volume giữ dữ liệu khi `docker compose down`. M1 chưa tạo bảng nghiệp vụ;
chưa có lệnh seed. Container web dùng Vite preview cho môi trường local.

Các port được bind vào loopback. Khi đổi API/web port, cập nhật tương ứng
`VITE_API_BASE_URL`, `CORS_ORIGINS` và rebuild web. URL `VITE_*` được đưa vào
bundle, chỉ chứa cấu hình công khai. Không đặt credential vào `VITE_*`.

```sh
docker compose ps
docker compose logs --tail=50 api web
docker compose down
```

## Phát triển trên host

Cần **Python 3.12**, **Node 22.12+** và npm. Không dùng Python mặc định
khác 3.12. `.env` phải tồn tại; `DATABASE_URL` dành cho API chạy trên host
và phải URL-encode mật khẩu nếu chứa ký tự đặc biệt.

```sh
cp .env.example .env  # Bỏ qua nếu đã có .env
make setup
docker compose up -d db
make api              # Terminal 1
make web              # Terminal 2
```

Dependency Python được chọn qua `requirements*.txt` và pin bằng
`services/api/requirements.lock`; npm dùng `package-lock.json` với `npm ci`.
Các gói hỗ trợ đã được duyệt: `react-dom`, `uvicorn`, `psycopg[binary]`,
`@types/react`, `@types/react-dom`. Không thêm thư viện test HTTP/DOM,
plugin React, parser ESLint TypeScript hay thư viện settings.

## Kiểm tra

Sau `make setup`:

```sh
make check             # ruff, ESLint, types, pytest, vitest, web build
make test-integration  # Cần database M1 riêng, trống, đang chạy
make migrate           # Kiểm tra Alembic; M1 chưa có revision nghiệp vụ
```

Không cần Python trên host nếu dùng image kiểm tra:

```sh
make check-docker      # ruff, generated types, pytest, PostgreSQL integration
npm ci
npm run lint
npm test
npm run build
```

`make check-docker` vẫn cần Node/npm cho các lệnh web riêng phía dưới.
Test integration chỉ nên trỏ vào database dành riêng cho M1, vì kiểm tra
schema không có bảng nghiệp vụ. `make down` dừng stack và giữ volume.

ESLint kiểm tra JavaScript sau khi TypeScript chuyển đổi. `tsc --noEmit`
kiểm tra kiểu, biến và tham số không dùng trực tiếp trên source. Cách này
giữ giới hạn dependency đã được yêu cầu; chưa có rule ESLint dành riêng cho TypeScript.

## Contract-first

1. Sửa `docs/openapi.json` trước khi thay đổi API.
2. Cập nhật model/handler FastAPI để khớp contract.
3. Chạy `npm run types:generate`, commit cả contract và `generated.ts`.
4. Chạy `make check`; CI phát hiện contract/type bị lệch.

`test_contract.py` so sánh chính xác OpenAPI runtime với contract.
Bộ sinh type chỉ dùng Python standard library, báo lỗi khi gặp cấu trúc
không hỗ trợ. Web sử dụng `Operations`/`Schemas` đã sinh để gọi API.

## Cấu trúc

```text
apps/web/             React + TypeScript + Vite
services/api/         FastAPI + SQLAlchemy + Alembic setup
infra/                Compose services, Dockerfile API/web
fixtures/             Chờ dữ liệu mô phỏng ở M2
docs/                 PRD, OpenAPI, NOTES, báo cáo milestone
tests/api/            pytest unit/contract/integration
scripts/              Sinh type và chạy ESLint không thêm plugin
.github/workflows/    CI lint + test + build
```

CI có hai job Python 3.12 và Node 22, với PostgreSQL service riêng; chạy
lint/format, contract/type check, API/web tests, Alembic check và build
cả hai container. Trạng thái run thực tế được ghi trong báo cáo milestone.

## Phạm vi tiếp theo

M2 schema + seed → M3 Auth/RBAC → M4 catalog → M5 map → M6 orders → M7 hardening.
Chỉ bắt đầu từng mốc sau khi được xác nhận. Xem [PRD](docs/PRD.md),
[quyết định phạm vi](docs/NOTES.md) và [báo cáo M1](docs/MILESTONE_M1.md).
ERD/WAREHOUSE_SIMULATION được viết ở M2; HACKATHON_SCOPE và tag
`pre-event-30` ở M7.

Không triển khai tính năng Phase B.
