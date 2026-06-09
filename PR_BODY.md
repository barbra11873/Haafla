Feature: Onboarding UX polish + portfolio uploads, validation, pagination, and S3-ready storage

Summary
- Adds client-side onboarding improvements (preview, resize, upload flow) on the frontend.
- Adds a backend portfolio upload endpoint for vendors and a paginated public portfolio listing endpoint.
- Implements server-side validation for uploaded images (type + size) and enforces vendor-only uploads.
- Adds DRF pagination (page size = 10) for portfolio listing.
- Adds S3-ready storage configuration (local by default, toggleable via `USE_S3` env var) and updates backend requirements to include `django-storages[boto3]` and `boto3`.
- Adds unit/integration tests for the backend and a basic frontend test scaffold for onboarding UI.

Endpoints added/modified
- `POST /api/vendors/portfolio/` — multipart/form-data endpoint to upload a `file`, `title`, and optional `description`. Requires authenticated vendor.
- `GET /api/vendors/portfolio-items/` — paginated list of portfolio items (public, supports `?page=`).
- `POST /api/vendors/vendors/` — vendor profile creation (existing behavior; view prevents duplicates)

Validation rules
- Allowed image content types: `image/jpeg`, `image/png`, `image/webp`.
- Max file size: 5MB.
- Only users with `role == 'vendor'` and an existing `Vendor` profile can upload portfolio items.

Storage
- Default: local storage (MEDIA_ROOT /media) and Django serves media in DEBUG.
- Production: set `USE_S3=1` and provide `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_STORAGE_BUCKET_NAME` to enable `storages.backends.s3boto3.S3Boto3Storage`. Add `django-storages[boto3]` + `boto3` to `backend/requirements.txt`.

Tests
- Backend: integration tests for JWT auth and vendors, and tests for portfolio upload endpoint (including multipart uploads).
- Frontend: Jest + React Testing Library scaffold with a basic onboarding test (requires installing dev deps locally).

Checklist
- [ ] validation working (image types + size)
- [ ] only vendors can upload
- [ ] pagination working (page size 10)
- [ ] S3 configured (when `USE_S3=1`)
- [ ] backend tests passing
- [ ] frontend tests passing (after `npm install` in `frontend/`)

Notes
- To open the PR on GitHub (branch is `onboarding-ux-polish`):
  https://github.com/barbra11873/Haafla/pull/new/onboarding-ux-polish
- The frontend tests require installing dev dependencies in `frontend/`:

  ```bash
  cd frontend
  npm install
  npm test
  ```

If you want, I can try to create the PR via the GitHub API/CLI, but the environment doesn't have `gh` installed — you can paste this body into the PR when you open it, or I can continue and attempt an authenticated PR creation if you provide a token.
