# Báo cáo M1 — Foundation

## Phần đã triển khai

- npm workspaces với `apps/web`, backend tại `services/api`.
- FastAPI/Pydantic v2: `/health`, `/health/ready`, lỗi JSON thống nhất
  `{code, message, details}`, CORS theo environment.
- PostgreSQL 16 trên Compose; readiness gọi `SELECT 1` qua SQLAlchemy 2.x.
- Dockerfile Python 3.12 và Node 22, container ứng dụng chạy user thường.
- Alembic setup, naming convention và metadata rỗng; chưa có bảng nghiệp vụ.
- OpenAPI viết trước API; test so sánh contract và sinh type cho frontend.
- React/TypeScript/Vite với TanStack Query, React Router, UI tiếng Việt,
  nhãn kho mô phỏng, trạng thái loading/error/retry và chưa có dữ liệu.
- Dependency lockfile cho Python và npm; `.env.example`, không commit `.env`.
- GitHub Actions cho lint, format, API/web tests, contract/types,
  PostgreSQL integration, Alembic và build API/web containers.

## Kiểm chứng local

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

## Commit và CI thực tế

| Commit | Nội dung |
| --- | --- |
| `ed1ae2c` | `feat(api): bootstrap contract-first FastAPI foundation` |
| `fa3eed5` | `feat(web): add Vietnamese foundation shell and local stack` |
| `3d85fa1` | `ci: validate M1 foundation and document milestone scope` |

[GitHub Actions run 41295856139](https://github.com/nvtank/AI-Intelligent-Warehouse-Management/actions/runs/41295856139)
đã **success** cho commit `3d85fa1dbbc80a6ed56035397254d4573b158f8e`:
API/Python 3.12 và Web/Node 22 đều passed, bao gồm build container.

Repo Git được khởi tạo riêng tại `mapflow`, dùng origin hiện có
`nvtank/AI-Intelligent-Warehouse-Management`; không stage các dự án cùng
thư mục cha. Source đã được push lên `main`. Chưa tạo tag M7.

## Chạy lại kiểm tra

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

## Toàn bộ file tạo trong M1

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

## Chưa làm

- M2: bảng nghiệp vụ, migrations nghiệp vụ, fixtures/seed idempotent,
  ERD.md và WAREHOUSE_SIMULATION.md.
- M3: Firebase Authentication, DEV_AUTH, Auth Emulator, users/roles/RBAC.
- M4: catalog CRUD, tìm không dấu, alias, ảnh và storage interface.
- M5: API map, SVG warehouse, bin detail, nodes/edges và kiểm tra đồ thị.
- M6: CRUD orders/items, state machine, deadline, audit.
- M7: xác nhận chạy từ máy sạch bằng đúng 3 lệnh gồm seed,
  HACKATHON_SCOPE.md, hash/tag và `pre-event-30`.
- Không có bất kỳ code, bảng hoặc endpoint Phase B nào.

Dừng sau M1; chưa được phép triển khai M2.
