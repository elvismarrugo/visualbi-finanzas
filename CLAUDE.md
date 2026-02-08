# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Siigo App is a full-stack ETL system that queries the Siigo accounting API, downloads Excel balance reports, transforms them, stores results in PostgreSQL, and exposes data via a Power BI-compatible API. The project language context is Spanish (Colombian accounting domain).

## Development Commands

### Backend (Python/FastAPI)

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python main.py                  # Runs on http://localhost:8000 with auto-reload
python init_db.py               # Initialize database tables
```

### Frontend (React/Vite)

```bash
cd frontend
npm install
npm run dev       # Dev server on http://localhost:5173
npm run build     # Production build
npm run lint      # ESLint
npm run preview   # Preview production build
```

### Database (PostgreSQL via Docker)

```bash
docker-compose up -d            # Start PostgreSQL on port 5432
```

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### No Test Framework

There are no automated tests. Manual testing is done via Swagger UI or the shell scripts (`probar_api.sh`).

## Architecture

```
Frontend (React 19 + Vite)          Backend (FastAPI + Uvicorn)
┌──────────────────────┐            ┌──────────────────────────┐
│ BalanceReportForm    │  axios     │ main.py (API routes)     │
│ DateRangeProcessor   │ --------> │ siigo_client.py (auth)   │
│ DataViewer           │            │ etl_service.py (ETL)     │
└──────────────────────┘            │ excel_processor.py       │
                                    │ database.py (SQLAlchemy) │
                                    └──────────┬───────────────┘
                                               │
                              ┌────────────────┼────────────────┐
                              │                │                │
                         Siigo API       PostgreSQL         SQLite
                         (external)      (primary)        (fallback)
```

### Backend modules

- **main.py** — FastAPI app, all route definitions, CORS config, startup logic
- **config.py** — Pydantic `Settings` class loading from `.env`
- **models.py** — Pydantic request/response schemas
- **siigo_client.py** — Async HTTP client for Siigo API authentication and report requests
- **etl_service.py** — Core ETL: month-by-month processing, token reuse, retry with backoff, deduplication
- **excel_processor.py** — Downloads Excel from Siigo URLs, finds header row, filters transactional rows, calculates derived columns (Movimiento, Cod Relacional, Periodo)
- **database.py** — SQLAlchemy ORM model `BalanceReport`, engine setup with PostgreSQL→SQLite fallback

### Frontend components

- **App.jsx** — Tab layout switching between the three main views
- **BalanceReportForm.jsx** — Single report query form with account range filters
- **DateRangeProcessor.jsx** — ETL batch processing UI with date range selection
- **DataViewer.jsx** — Paginated data browser with filtering and stats

### Data flow

1. User selects date range → React sends POST to `/api/etl/process-date-range`
2. Backend authenticates once with Siigo, reuses token
3. For each month: requests report → downloads Excel → parses with pandas → transforms → inserts into PostgreSQL
4. DataViewer fetches processed data from `/api/powerbi/balance-reports`

### Key ETL logic

- Header detection: searches for row containing "Nivel" and "Código cuenta contable"
- Row filter: keeps only `Transaccional = "Sí"` or `"SI"`
- Derived fields: `Movimiento = Débito - Crédito`, `Cod Relacional = first 6 chars of account code`, `Periodo = YYYYMM`
- Month 13 is treated as annual close (date set to Dec 31)

## Environment Variables

Configured in `.env` at project root (never committed):

```
SIIGO_ACCESS_KEY, SIIGO_PARTNER_ID, SIIGO_BASE_URL, SIIGO_USERNAME
BACKEND_PORT
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
```

## Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/balance-report-by-thirdparty` | POST | Direct Siigo report query |
| `/api/etl/process-year` | POST | ETL process for a calendar year |
| `/api/etl/process-previous-year` | POST | ETL process for previous year |
| `/api/etl/process-date-range` | POST | ETL process for arbitrary date range |
| `/api/powerbi/balance-reports` | GET | Query stored data (filters: año, periodo, account) |
| `/api/powerbi/stats` | GET | Aggregated statistics |

## CORS

Backend allows origins on localhost ports 3000, 5173–5177. Update `main.py` if using a different frontend port.
