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

## Upload storage and media configuration

By default, uploaded media is stored locally under `backend/media/` and served in development mode.

To switch to S3 in production, set:

```bash
USE_S3=1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_REGION_NAME=...
AWS_S3_CUSTOM_DOMAIN=...   # optional
```

Backend requirements for media handling include `Pillow` for image validation and thumbnail generation, and `django-storages[boto3]` + `boto3` for S3 storage.

The portfolio API now exposes:

- `POST /api/vendors/portfolio/` for authenticated vendor uploads
- `GET /api/vendors/portfolio-items/` for paginated portfolio browsing

Uploaded images are validated server-side, resized into thumbnails, and stored alongside the original image.
