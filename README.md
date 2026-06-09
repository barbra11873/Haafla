# EventChain AI

Monorepo scaffold for EventChain AI — an AI-powered event marketplace with blockchain-backed trust and escrow.

This scaffold contains a minimal Django backend and a Next.js frontend to get development started.

See `docs/architecture.md` for full system design.

## Quick start (development)

Prerequisites: Python 3.10+, Node 18+, Docker (optional)

Backend (local venv):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend (local):

```bash
cd frontend
npm install
npm run dev
```
