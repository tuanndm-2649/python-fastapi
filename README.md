# TaskHub API

Backend quản lý project và task, sử dụng FastAPI, SQLAlchemy và PostgreSQL.

## Yêu cầu

- Python 3.15 trở lên
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL đang chạy

## Cài đặt

```bash
uv sync
cp .env.example .env
```

Tạo tài khoản và database PostgreSQL, sau đó cập nhật `.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```

Không commit file `.env` chứa thông tin thật.

## Chạy migration

```bash
uv run alembic upgrade head
```

## Chạy ứng dụng

```bash
uv run uvicorn demo_fastapi.main:app --reload
```

- Health check: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs

## Khi thay đổi model

```bash
uv run alembic revision --autogenerate -m "describe schema change"
```

Kiểm tra file migration vừa sinh trong `alembic/versions/`, rồi áp dụng:

```bash
uv run alembic upgrade head
```

## Cấu trúc chính

```text
src/demo_fastapi/
├── main.py       # Khởi tạo ứng dụng
├── database.py   # Kết nối database và session
├── models/       # SQLAlchemy models
├── schemas/      # Schema dữ liệu API
├── crud/         # Thao tác database
└── routers/      # API endpoints

alembic/          # Cấu hình và lịch sử migration
```
