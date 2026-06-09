Feature: Portfolio image hardening, thumbnails, pagination, S3-ready storage, and onboarding tests

Summary
- Adds client-side onboarding improvements (preview, resize, upload flow) on the frontend.
- Adds a backend portfolio upload endpoint for vendors and a paginated public portfolio listing endpoint.
- Hardens image uploads server-side with content sniffing, corruption rejection, 5MB limit, and 3000x3000 dimension limit.
- Auto-generates and stores thumbnails for each uploaded portfolio image.
- Adds DRF pagination (page size = 10) for portfolio listing.
- Adds S3-ready storage configuration (local by default, toggleable via `USE_S3` env var) and updates backend requirements to include `Pillow`, `django-storages[boto3]`, and `boto3`.
- Adds backend upload tests plus frontend Jest/RTL onboarding tests.

Endpoints added/modified
- `POST /api/vendors/portfolio/` — multipart/form-data endpoint to upload a `file`, `title`, and optional `description`. Requires authenticated vendor.
- `GET /api/vendors/portfolio-items/` — paginated list of portfolio items (public, supports `?page=`).
- `POST /api/vendors/vendors/` — vendor profile creation (existing behavior; view prevents duplicates)

Validation rules
- Allowed image formats: jpg, png, webp.
- Max file size: 5MB.
- Max dimensions: 3000x3000.
- Corrupted or invalid images are rejected.
- Only users with `role == 'vendor'` and an existing `Vendor` profile can upload portfolio items.

Storage
- Default: local storage (`MEDIA_ROOT` under `/media`) and Django serves media in DEBUG.
- Production: set `USE_S3=1` and provide `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_STORAGE_BUCKET_NAME` to enable `storages.backends.s3boto3.S3Boto3Storage`.
- Optional: set `AWS_S3_REGION_NAME` and `AWS_S3_CUSTOM_DOMAIN` for bucket/CDN routing.

Tests
- Backend: integration tests for JWT auth and vendors, upload validation tests, thumbnail generation checks, and multipart upload tests.
- Frontend: Jest + React Testing Library onboarding tests for validation, loading state, and successful upload flow.

Checklist
- [ ] validation working (content sniffing + size + dimensions)
- [ ] only vendors can upload
- [ ] thumbnail generation working
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

If you want, I can try to create the PR via the GitHub UI, but the environment doesn't have `gh` installed and there is no GitHub token configured here.
