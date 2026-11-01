# Báo cáo hoàn thành M1 — MapFlow AI, Phase A

**Mốc báo cáo:** M1 — Foundation.

**Ngày ghi nhận kết quả M1:** 01/11/2026.

**Trạng thái:** M1 đã hoàn thành; đang chờ xác nhận để bắt đầu M2.

## 1. Mục tiêu và phạm vi báo cáo

MapFlow AI hướng tới quản lý kho vật liệu xây dựng mô phỏng, bao gồm danh mục
vật liệu, vị trí trong kho và đơn nhập/xuất. M1 xây dựng nền tảng để những
chức năng này có thể được triển khai, kiểm thử và chạy nhất quán ở các mốc sau.

**30% là phạm vi mục tiêu của toàn Phase A, không phải tỷ lệ đã hoàn thành
sau M1.** Phase A gồm năm hạng mục dưới đây. M1 hoàn thành phần khởi tạo
foundation; schema và seed thuộc M2 nên chưa thể ghi nhận toàn bộ Foundation
6% là đã hoàn thành.

| Hạng mục Phase A | Tỷ trọng theo kế hoạch | Trạng thái sau M1 |
| --- | --- | --- |
| Foundation | 6% | Đã có nền tảng chạy; còn schema và seed ở M2 |
| Auth & RBAC | 4% | Chưa triển khai; dự kiến M3 |
| Product Catalog | 7% | Chưa triển khai; dự kiến M4 |
| Basic Warehouse Map | 8% | Chưa triển khai; dự kiến M5 |
| Basic Orders | 5% | Chưa triển khai; dự kiến M6 |
| **Tổng phạm vi Phase A** | **30%** | **Chưa hoàn thành toàn Phase A** |

M7 kiểm tra và chốt điều kiện nghiệm thu của toàn Phase A. Các yêu cầu gốc
được ghi trong [PRD](PRD.md); quyết định kỹ thuật và giới hạn hiện tại được
ghi trong [NOTES](NOTES.md).

## 2. Chức năng và nền tảng đã hoàn thành

### 2.1. Cấu trúc dự án và môi trường chạy

| Thành phần | Kết quả đã có |
| --- | --- |
| Monorepo | npm workspaces; web tại `apps/web`, API tại `services/api`; tách `infra`, `fixtures`, `docs`, `tests` |
| Web | React + TypeScript + Vite; đã tích hợp TanStack Query và React Router |
| API | FastAPI, Pydantic v2, application factory và quản lý vòng đời kết nối database |
| Database | PostgreSQL 16 chạy bằng Docker Compose; kết nối qua SQLAlchemy 2.x và psycopg |
| Migration | Alembic setup, metadata rỗng, quy ước đặt tên constraint; chạy được `upgrade head` và `check` |
| Container | Dockerfile API dùng Python 3.12, web dùng Node 22; ứng dụng chạy bằng user thường |
| Cấu hình | `.env.example`, CORS theo environment, cấu hình port và URL API; `.env` bị gitignore |
| Dependency | Lockfile Python và npm để tái lập các phiên bản đã kiểm tra |
| Lệnh vận hành | Makefile cho setup, chạy dịch vụ, migration, sinh type, lint, test và build |

Compose khởi động database trước, đợi API sẵn sàng rồi chạy web. Volume
PostgreSQL giữ dữ liệu khi dừng stack bằng `docker compose down`.
Hiện chưa có bảng nghiệp vụ, revision nghiệp vụ hay dữ liệu seed.

### 2.2. API kiểm tra hoạt động

| Endpoint | Chức năng đã hoàn thành | Kết quả |
| --- | --- | --- |
| `GET /health` | Kiểm tra tiến trình API, không phụ thuộc database | HTTP 200, tên dịch vụ, phiên bản và `simulation: true` |
| `GET /health/ready` | Thực hiện `SELECT 1` trên PostgreSQL | HTTP 200 nếu kết nối được; HTTP 503 nếu thiếu cấu hình hoặc database không truy cập được |
| `/docs`, `/redoc`, `/openapi.json` | Cung cấp tài liệu và schema API qua FastAPI | Có thể tra cứu contract hiện tại |

API đã có cơ chế trả lỗi thống nhất cho lỗi HTTP, validation và lỗi hệ thống.
Ví dụ khi database chưa sẵn sàng:

```json
{
  "code": "DATABASE_UNAVAILABLE",
  "message": "Chưa kết nối được PostgreSQL.",
  "details": null
}
```

Health endpoint hiện công khai. Xác thực và bảo vệ API nghiệp vụ sẽ được
triển khai ở M3. Nguồn triển khai: [API main](../services/api/app/main.py).

### 2.3. Contract giữa frontend và backend

- Đã viết [OpenAPI contract](openapi.json) cho hai endpoint health trước
  khi triển khai handler tương ứng.
- Backend có test so sánh chính xác OpenAPI runtime với contract đã commit.
- Bộ sinh type dùng Python standard library, xuất `Schemas` và `Operations`
  cho TypeScript; báo lỗi khi gặp cấu trúc schema chưa hỗ trợ.
- API client của web sử dụng type đã sinh; hỗ trợ truyền tín hiệu hủy request
  và biểu diễn lỗi API cho giao diện.
- CI kiểm tra file type đã sinh còn khớp contract.

### 2.4. Kiểm tra tự động

GitHub Actions có hai job: API/Python 3.12 và Web/Node 22. Workflow chạy
ruff, kiểm tra format, TypeScript, ESLint, pytest, vitest, contract/type check,
PostgreSQL integration, Alembic và build hai container.

ESLint hiện kiểm tra JavaScript sau khi TypeScript chuyển đổi;
`tsc --noEmit` kiểm tra kiểu và các biến/tham số không dùng trên source.
Giới hạn này được ghi nhận để tuân thủ danh sách dependency đã được duyệt.

## 3. Giao diện đã hoàn thành

### 3.1. Trang nền tảng và điều hướng

Trang `/` đã có bố cục hoàn chỉnh cho mốc M1, dùng nền sáng và màu xanh đậm,
nội dung tiếng Việt. Đây là trang giới thiệu trạng thái phát triển hiện tại.

| Khu vực giao diện | Nội dung và hành vi đã có |
| --- | --- |
| Header | Logo chữ MapFlow AI, liên kết về trang chủ và nhãn “KHO MÔ PHỎNG” |
| Phần giới thiệu | Tiêu đề, mô tả mục tiêu hệ thống và thông báo “Không sử dụng dữ liệu kho thật” |
| Lộ trình | Sáu thẻ M1–M6; M1 được nhấn mạnh, M2–M6 ghi “Chưa triển khai”; có ghi chú M7 kiểm tra hoàn thiện |
| Thông báo dữ liệu | Hiển thị rõ chưa có dữ liệu kho, dữ liệu mẫu sẽ bổ sung ở M2 |
| Kết nối API | Gọi `/health` bằng TanStack Query và hiển thị phiên bản API khi thành công |
| Footer | Tên dự án và nhãn “Phase A · M1 Foundation” |
| Trang không tồn tại | Route dự phòng hiển thị “Không tìm thấy trang” và liên kết về trang chủ |

Các thẻ lộ trình chỉ trình bày kế hoạch. Chưa có màn hình đăng nhập,
danh sách sản phẩm, bản đồ SVG hay màn hình quản lý đơn.

### 3.2. Các trạng thái giao diện

| Trạng thái | Hiển thị đã triển khai |
| --- | --- |
| Đang tải | “Đang kiểm tra kết nối API…” |
| Kết nối thành công | Chấm trạng thái xanh, “API đang hoạt động” và phiên bản API |
| Lỗi kết nối | Thông báo chưa kết nối được API, kèm nút “Thử lại” để gọi lại request |
| Chưa có dữ liệu | Thông báo chưa có dữ liệu kho ở mốc hiện tại |

Đây là trạng thái của trang foundation và kết nối API. Các trạng thái
loading/empty/error cho catalog, map và orders sẽ được xây dựng cùng từng
màn hình nghiệp vụ.

### 3.3. Responsive và khả năng sử dụng

- Lưới thẻ dùng ba cột trên màn hình lớn, hai cột ở chiều rộng tối đa 900 px
  và một cột ở chiều rộng tối đa 560 px.
- Có khai báo ngôn ngữ `vi`, viewport, liên kết bỏ qua header để đến nội dung
  chính và focus indicator cho thao tác bàn phím.
- Trạng thái kết nối dùng `role="status"`; lỗi kết nối dùng `role="alert"`.
- Đã kiểm tra hiển thị bằng Chromium ở chiều rộng 1024 px trong lần nghiệm
  thu M1, xác nhận trang hiển thị tiếng Việt và kết nối được API.

Chưa có bộ kiểm thử tương tác trình duyệt tự động hoặc đánh giá accessibility
đầy đủ. Test web hiện kiểm tra API client và nội dung render tĩnh của trang.
Nguồn giao diện: [App](../apps/web/src/App.tsx),
[HealthStatus](../apps/web/src/HealthStatus.tsx),
[styles](../apps/web/src/styles.css).

## 4. Kết quả kiểm chứng M1

Các kết quả sau được ghi nhận trong lần nghiệm thu M1; lần cập nhật báo cáo
này chỉ thay đổi tài liệu.

| Kiểm tra | Kết quả |
| --- | --- |
| Python 3.12: pytest unit + contract | 7 passed |
| Python 3.12: PostgreSQL integration | 1 passed |
| Vitest | 5 passed |
| ruff check + format | Passed |
| tsc + ESLint | Passed |
| OpenAPI generated types | Khớp contract |
| Vite production build | Passed |
| Alembic upgrade head + check | Không có schema drift |
| Workflow actionlint | Passed |
| Compose `up --build -d --wait` | db/api/web đều healthy |
| Live HTTP | Health, readiness và web shell tiếng Việt passed |
| Giao diện tablet 1024 px | Đã kiểm tra bằng Chromium, kết nối API thành công |

### 4.1. Commit và CI thực tế

| Commit | Nội dung |
| --- | --- |
| `ed1ae2c` | `feat(api): bootstrap contract-first FastAPI foundation` |
| `fa3eed5` | `feat(web): add Vietnamese foundation shell and local stack` |
| `3d85fa1` | `ci: validate M1 foundation and document milestone scope` |
| `edb3a42` | `docs: record verified M1 CI results` |

[GitHub Actions run 41295969604](https://github.com/nvtank/AI-Intelligent-Warehouse-Management/actions/runs/41295969604)
đã **success** cho commit `edb3a42e627d9928d8932b69921ce5c78b77679f`:
API/Python 3.12 và Web/Node 22 đều passed, bao gồm build container.

Repo Git được khởi tạo riêng tại `mapflow`, dùng origin hiện có
`nvtank/AI-Intelligent-Warehouse-Management`; không stage các dự án cùng
thư mục cha. Source đã được push lên `main`. Chưa tạo tag M7.

### 4.2. Cách xem và kiểm tra lại

Khởi động từ thư mục gốc của dự án, nếu chưa có cấu hình local:

```sh
cp .env.example .env
# Sửa mật khẩu PostgreSQL trong .env trước khi chạy.
docker compose up --build -d --wait
```

Nếu `.env` đã tồn tại, giữ cấu hình đang dùng và bỏ qua bước sao chép.
Truy cập web tại <http://localhost:5173>, tài liệu API tại
<http://localhost:8000/docs>. Hướng dẫn môi trường và cấu hình chi tiết nằm
trong [README](../README.md).

```sh
# Sau khi có .env; không cần Python 3.12 trên host:
make check-docker
npm ci
npm run lint
npm test
npm run build
```

Hoặc sau `make setup`: `make check` và `make test-integration`.
API integration yêu cầu database dành riêng cho M1.

## 5. Danh sách file của M1

Không có source cũ để sửa. Tất cả các file sau được tạo mới.

```text
.dockerignore
.editorconfig
.env.example
.github/workflows/ci.yml
.gitignore
Makefile
README.md
compose.yaml
eslint.config.mjs
package.json
package-lock.json
pyproject.toml
apps/web/index.html
apps/web/package.json
apps/web/tsconfig.json
apps/web/vite.config.mjs
apps/web/src/App.tsx
apps/web/src/App.test.tsx
apps/web/src/HealthStatus.tsx
apps/web/src/main.tsx
apps/web/src/styles.css
apps/web/src/api/client.ts
apps/web/src/api/client.test.ts
apps/web/src/api/generated.ts
services/api/requirements.txt
services/api/requirements-dev.txt
services/api/requirements.lock
services/api/alembic.ini
services/api/alembic/env.py
services/api/alembic/script.py.mako
services/api/alembic/versions/.gitkeep
services/api/app/__init__.py
services/api/app/config.py
services/api/app/database.py
services/api/app/main.py
services/api/app/schemas.py
infra/compose.yaml
infra/Dockerfile.api
infra/Dockerfile.web
scripts/generate_web_types.py
scripts/lint-web.mjs
fixtures/README.md
tests/api/conftest.py
tests/api/test_contract.py
tests/api/test_foundation.py
docs/PRD.md
docs/NOTES.md
docs/openapi.json
docs/MILESTONE_M1.md
```

`.env` là cấu hình local bị gitignore; build output, node_modules và ảnh
kiểm tra giao diện không thuộc source được commit.

## 6. Phần chưa hoàn thành và hướng phát triển

### 6.1. M2 — Schema và dữ liệu mô phỏng

Mục tiêu tiếp theo là xây dựng cơ sở dữ liệu nghiệp vụ đủ để phát triển
auth, catalog, map và orders:

- Tạo models và migrations cho identity, warehouse, indoor map, catalog,
  orders, lịch sử trạng thái và audit theo data model đã duyệt.
- Áp dụng FK, unique, check constraint; mã vị trí đầy đủ phải unique;
  bin phải gắn node hợp lệ của map version đang active.
- Seed idempotent một kho với 3 zone, 4 aisle, khoảng 20 bin, mỗi rack
  3–4 level và đồ thị nodes/edges liên thông.
- Seed 30 SKU có alias tiếng Việt, các trường hợp tên dễ gây mơ hồ và đủ
  golden case: gạch, vít 50 mm, khung thép 2 m.
- Seed 10–15 đơn có deadline/trạng thái khác nhau và ba user cho ba role.
- Đánh dấu mọi dữ liệu seed là mô phỏng; thêm `make seed` và
  `python -m app.seed`; viết `ERD.md`, `WAREHOUSE_SIMULATION.md`.

### 6.2. M3 — Đăng nhập và phân quyền

- Xác thực Firebase ID token ở backend, role lấy từ database.
- Bổ sung DEV_AUTH cho local và hướng dẫn Auth Emulator tùy chọn.
- Triển khai `/auth/me`, kiểm tra user active, dependency `require_roles`.
- Tạo trang đăng nhập, route guard và menu theo role.
- Test role × endpoint, bao gồm 401/403: Admin toàn quyền, Manager đọc
  catalog/map và CRUD đơn, Operator chỉ đọc/tìm kiếm theo phạm vi đã duyệt.

### 6.3. M4 — Danh mục vật liệu

- API và UI CRUD SKU, categories, units, alias, quy cách,
  trọng lượng/kích thước.
- Tìm kiếm tên/SKU/alias không dấu, lọc category và phân trang.
- Upload ảnh qua storage interface, local lưu disk; soft-delete product
  và giữ tính toàn vẹn với đơn hàng.
- Thêm trang chi tiết sản phẩm, loading/empty/error state, audit cho
  thay đổi catalog và test quyền/validation/tìm “vit 50mm”.

### 6.4. M5 — Bản đồ kho 2D

- Triển khai API warehouse, zones, aisles, bins và map.
- Vẽ SVG zone/aisle/rack/bin; click bin mở panel vị trí và các level của rack.
- Cho phép bật/tắt hiển thị nodes/edges; kiểm tra dữ liệu và tính liên thông.
- Chỉ hiển thị đồ thị; không triển khai thuật toán đường đi.

### 6.5. M6 — Đơn nhập/xuất cơ bản

- API và UI CRUD đơn/dòng hàng, chọn sản phẩm bằng tìm kiếm, deadline,
  lọc trạng thái và deadline.
- Backend kiểm soát chuyển trạng thái hợp lệ; lưu lịch sử và audit
  cùng thay đổi nghiệp vụ trong transaction.
- Test quyền, validation, chuyển trạng thái và audit; hoàn thiện trạng thái
  tải, rỗng, lỗi cho màn hình đơn.

### 6.6. M7 — Hoàn thiện và nghiệm thu Phase A

- Kiểm chứng Compose, migration và seed từ máy sạch; README chạy bằng
  đúng ba lệnh, bao gồm seed.
- Rà soát giao diện tablet, xử lý lỗi, constraint và quyền API trên toàn hệ thống.
- Chạy đầy đủ lint/test/build và xác nhận CI xanh; rà lại các giới hạn kỹ thuật
  đã ghi trong NOTES.
- Viết `HACKATHON_SCOPE.md` với chức năng thực tế và commit hash;
  tạo tag `pre-event-30` sau khi đủ điều kiện.

### 6.7. Nguyên tắc cho các mốc tiếp theo

Mỗi mốc phải sửa OpenAPI trước khi triển khai API, sinh lại type web,
kiểm tra dữ liệu ở backend và ghi audit cho các thay đổi nghiệp vụ theo yêu cầu.
Khi hoàn thành phải báo cáo file đã tạo/sửa, lệnh test và phần còn thiếu,
rồi dừng chờ xác nhận trước mốc tiếp theo.

Các chức năng Phase B như Agent, tồn theo lô, route, xe nâng, picking,
QR, Document AI, FCM và analytics không thuộc đợt triển khai này.
Chưa có code, bảng hoặc endpoint dự phòng cho các phần đó. Nếu xem xét
trong tương lai, phải có phạm vi và phê duyệt riêng sau Phase A.

**Trạng thái bàn giao: hoàn thành M1; chưa bắt đầu M2 và chưa đạt toàn bộ
định nghĩa hoàn thành 30% của Phase A.**
