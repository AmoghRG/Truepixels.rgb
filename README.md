# TruePixels.rgb

**AI-Generated Image Detection Platform** — FastAPI backend + React frontend with JWT authentication, image validation/preprocessing, and request-level latency observability.

---

## Features

- **Authentication & RBAC (`app/m1_access/`)**: User registration, login, and admin seeding (`seed_admin.py`) using Argon2/bcrypt password hashing and JWT (`python-jose`).
- **Image Ingestion & Preprocessing**: Multipart upload endpoint with strict file validation, `Pillow`/`NumPy` preprocessing, and managed local storage (`storage/`).
- **API Observability & Error Handling (`app/shared/`)**: Global exception handlers, automatic `X-Request-ID` correlation headers, and `X-Process-Time-Ms` server latency tracking.
- **Database & Migrations**: SQLAlchemy 2.0 ORM with Alembic schema migrations.
- **Tested API Surface (`tests/`)**: Async integration tests powered by `pytest`, `pytest-asyncio`, and `httpx`.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0, Alembic
- **Security:** `argon2-cffi`, `passlib[bcrypt]`, `python-jose`
- **Image Processing:** Pillow, NumPy
- **Frontend:** React (`frontend/`)
- **Testing:** `pytest`, `pytest-asyncio`, `httpx`

---

## Project Structure

```text
├── app/
│   ├── main.py             # FastAPI entrypoint, CORS, request-ID & timing middleware
│   ├── m1_access/          # Auth, user management, image upload, validation & preprocessing
│   └── shared/             # Database setup & structured error handlers
├── frontend/               # React client application
├── storage/                # Uploaded & processed image storage
├── tests/                  # Automated API tests
├── seed_admin.py           # Admin user bootstrap script
├── requirements.txt
└── .env.example
```

---

## Quickstart

```bash
# 1. Configure environment
cp .env.example .env

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Seed admin account & start the API server
python seed_admin.py
uvicorn app.main:app --reload
```

Interactive API docs are available at `http://localhost:8000/docs`.

```bash
# Run tests
pytest
```
