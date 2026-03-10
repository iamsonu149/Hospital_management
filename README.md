# Hospital Management

Full-stack healthcare appointment platform with role-based access (`admin`, `doctor`, `patient`), doctor availability and slot booking, patient history tracking, JWT auth, and async background jobs (CSV export + scheduled reminders/reports).

## Tech Stack

- Backend: Flask, SQLAlchemy, JWT, Celery
- Frontend: Vue (Vite)
- Queue/Broker: Redis
- Email testing: MailHog (SMTP + UI)
- Database: SQLite (`backend/instance/optimus.sqlite3`)

## Prerequisites

- Python 3.10+ (recommended: 3.12)
- Node.js 18+
- Redis server
- MailHog (optional, for local email testing)

## Project Setup (WSL/Linux)

### 1) Clone

```bash
git clone git@github.com:iamsonu149/Hospital_management.git
cd Hospital_management
```

### 2) Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3) Frontend setup

```bash
cd ../frontend
npm install
```

## Running the Project

Start each service in a separate terminal.

### Terminal A: Redis

```bash
redis-cli ping
```

If you do not get `PONG`, start Redis:

```bash
redis-server
```

### Terminal B: Flask backend

```bash
cd backend
source venv/bin/activate
python3 app.py
```

Backend runs on: `http://127.0.0.1:5000`

### Terminal C: Celery worker

```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker -l info
```

### Terminal D: Celery beat (for scheduled jobs)

```bash
cd backend
source venv/bin/activate
celery -A app.celery_app beat -l info
```

### Terminal E: Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://127.0.0.1:5173` (or `http://localhost:5173`)

## MailHog (Optional, for email testing)

Mail code is configured for:
- SMTP host: `localhost`
- SMTP port: `1025`

Start MailHog:

```bash
MailHog
```

If `MailHog` command is not in PATH, run the installed binary path (example):

```bash
~/go/bin/MailHog
```

MailHog UI:
- `http://localhost:8025`

## Background Jobs in this Project

- Daily reminder job
- Monthly activity report mail to doctors
- User-triggered async CSV export for patient treatment history

## Common Troubleshooting

### Redis: `Address already in use` on 6379

Redis is already running. Do not start a second instance.

```bash
redis-cli ping
```

### Redis: `MISCONF ... unable to persist to disk`

Quick dev workaround:

```bash
redis-cli config set stop-writes-on-bgsave-error no
```

### Celery periodic jobs not running

Make sure both worker and beat are running.  
After schedule changes, restart beat.

### VS Code Python warnings (`Pylance`)

Set interpreter to:

`backend/venv/bin/python`

## Windows Notes

If working on Windows native shell (not WSL), activate venv with:

```powershell
venv\Scripts\activate
```
