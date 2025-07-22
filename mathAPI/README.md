# Math Microservice

This repository contains a FastAPI-based microservice that performs basic mathematical operations (power, Fibonacci, factorial), persists all requests to a SQLite database, and provides both a JSON API (JWT‑protected) and an HTML frontend (session‑cookie protected). It is containerized via Docker for easy deployment.

---

##  Project Structure

```
mathAPI/                   # Project root
├── Dockerfile             # Container build instructions
├── docker-compose.yml     # (Optional) Compose setup for dev
├── .dockerignore          # Files to exclude from Docker build
├── requirements.txt       # Python dependencies
├── main.py                # FastAPI app entrypoint
├── frontend/              # Static HTML/JS UI
│   ├── login.html         # Login page
│   └── math.html          # Math operations UI
├── app/                   # Backend application code
│   ├── api/               # API routers
│   │   ├── auth.py        # JWT login endpoints
│   │   └── frontend.py    # Session‑cookie HTML routes
│   ├── controllers/       # JSON API handlers
│   │   └── math_controller.py
│   ├── models/            # Database and ORM models
│   │   ├── database.py    # DB session & engine setup
│   │   └── models.py      # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas for request/response
│   │   └── schemas.py
│   └── services/          # Pure Python compute logic (pow, fib, fact)
│       └── math_service.py
└── README.md              # This file
```

---

##  Quick Start

### Prerequisites

* Python 3.11+ (local development)
* Docker (for containerized deployment)

### Local (venv)

```bash
# 1. Clone and enter repo
git clone <repo-url> && cd mathAPI

# 2. Create & activate venv
python -m venv .venv
. .venv/Scripts/activate     # PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
data/db.sqlite3               # SQLite will auto-create
uvicorn main:app --reload
```

Then point your browser to `http://127.0.0.1:8000/` to access the login UI.

### Docker

```bash
# Build the image
docker build -t math-microservice .

# Run the container
docker run -d -p 8000:8000 --name mathsvc math-microservice
```

Open `http://localhost:8000/` in your browser.

(Optional) using Docker Compose:

```bash
docker-compose up --build
```

---

##  Usage

### 1. HTML Frontend

1. **Login** via `login.html` (username: `admin`, password: `password`).
2. **Math** operations at `math.html`—Fibonacci, Power, Factorial.

### 2. JSON API (JWT‑Protected)

All endpoints require an `Authorization: Bearer <token>` header obtained via:

```bash
POST /login  # form‑urlencoded, returns { access_token }
```

| Endpoint                | Method | Query / Body          | Response       |
| ----------------------- | ------ | --------------------- | -------------- |
| `/api/v1/pow?x=2&y=3`   | POST   | Query params `x`, `y` | `{result: 8}`  |
| `/api/v1/fibonacci/{n}` | GET    | Path param `n` (≥0)   | `{result: 8}`  |
| `/api/v1/factorial?n=5` | GET    | Query param `n` (≥0)  | `{result:120}` |

---

##  Docker

* **Dockerfile** builds a lightweight image on `python:3.11-slim`.
* Installs all Python dependencies from `requirements.txt`.
* Exposes port `8000` and runs Uvicorn on container start.

Optional **docker-compose.yml** mounts code as a volume for live reload and maps port `8000:8000`.

---

##  Authentication

* **HTML UI** uses a simple session cookie (`authenticated=yes`, 30min expiry) set after posting to `/login-form`.
* **JSON API** uses JWTs:

  * Obtain via `POST /login` (OAuth2PasswordRequestForm).
  * Protected endpoints depend on `oauth2_scheme` + `verify_token()`.

---

##  Extensibility & Nice‑to‑Haves

* **Database:** SQLite by default; swap for PostgreSQL/MySQL by updating `DATABASE_URL` in `database.py`.
* **Containerization:** Dockerized; adds portability.
* **Caching:** easily insert `functools.lru_cache` or Redis.
* **Monitoring:** attach Prometheus exporter, Grafana dashboards.
* **Logging:** configure `logging` to stream through Kafka/RabbitMQ.
* **Authorization:** integrate OAuth2 scopes or roles in `auth.py`.

---

