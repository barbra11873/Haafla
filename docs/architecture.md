# EventChain AI — System Architecture

This document describes the architecture for EventChain AI, including backend app boundaries, frontend structure, database overview, API endpoints, AI and blockchain integration points.

## Backend (Django) — High level

We structure the backend as several Django apps, each owning related models, serializers, views and tests:

- `core` — common utilities, custom `User` model (roles), base permissions.
- `vendors` — vendor profiles, portfolios, availability, verification status.
- `marketplace` — service listings, categories, search indexing.
- `bookings` — booking lifecycle, status transitions, messaging hooks.
- `payments` — escrow records, integration with Stripe and blockchain bridges.
- `ai` — wrappers for AI prompt templates, orchestration endpoints.
- `blockchain` — blockchain adapter, transaction log, on-chain sync tasks.
- `admin` — admin utilities and dispute resolution helpers.

Each app exposes REST endpoints via Django REST Framework. Authentication uses JWT (SimpleJWT).

## Frontend (Next.js)

Project layout:

- `pages/` — route-based pages: `/`, `/login`, `/signup`, `/vendors/[id]`, `/bookings/[id]`, `/planner`.
- `components/` — shared UI components (Layout, Header, VendorCard, BookingForm).
- `lib/api.js` — small wrapper around `fetch`/`axios` for calling backend endpoints and attaching JWT.
- `hooks/` — React hooks (useAuth, useSWR hooks for data fetching).
- `styles/` — global CSS / Tailwind config.

Frontend communicates with backend REST APIs and calls AI endpoints for planner interactions.

## Database overview

Primary datastore: PostgreSQL (development may use SQLite). Core entities:

- `User` (id, email, password_hash, role{customer,vendor,admin}, profile data)
- `Vendor` (id, user_id, name, verified, rating, portfolio[])
- `Service` (id, vendor_id, category, title, description, price, availability calendar)
- `Booking` (id, customer_id, service_id, status, start_time, end_time, total_amount, escrow_locked)
- `Payment`/`Escrow` (id, booking_id, amount, provider_tx, on_chain_tx, status)
- `Review` (id, booking_id, rating, text, verified_on_chain)

Indexes: users.email unique, services.category, vendor.rating, bookings.status

## API structure (sample)

- `POST /api/auth/signup/` — create account
- `POST /api/auth/login/` — returns JWT access & refresh
- `GET /api/vendors/` — list vendors (filters: category, location, rating)
- `GET /api/vendors/{id}/` — vendor profile
- `POST /api/services/` — vendor adds a service (vendor auth)
- `POST /api/bookings/` — customer creates booking (creates escrow record)
- `POST /api/bookings/{id}/accept/` — vendor accepts booking
- `POST /api/payments/checkout/` — starts payment flow (Stripe)
- `POST /api/ai/plan/` — generate event plan (AI)
- `POST /api/blockchain/verify_review/` — anchor review on-chain

Authentication: JWT in `Authorization: Bearer <token>` header.

## AI integration layer

AI will be used for two purposes:

1. Planning orchestration — given event type, budget, guest count, location, return a structured plan: timeline, suggested vendors, budget allocation.
2. Recommendations/reranking — use embeddings to match user needs to vendor offerings.

Design:
- `ai` Django app wraps calls to chosen LLM provider (OpenAI, etc.).
- Prompt templates stored and versioned; responses normalized into JSON schema.
- Rate limiting and caching for repeated queries.
- Protect PII: remove or hash sensitive fields before sending to provider.

## Blockchain integration layer

Blockchain responsibilities:

- Escrow smart contract to lock funds until event completion.
- Anchor verified reviews to an on-chain log.
- Optionally mint NFT tickets.

Design:
- Keep blockchain interactions in `blockchain` app which maintains a queue of actions to submit on-chain.
- Off-chain DB mirrors transaction status and stores provider Tx hashes.
- Use a light-weight signer service or wallet integration for admin/operator actions.

## Deployment

- Dockerize backend and frontend, use Kubernetes or Docker Compose for small deployments.
- CI: Lint + unit tests + build frontend static export.

## Next steps

1. Create ER diagrams and detailed field lists for each model.
2. Define API schemas (OpenAPI) and generate client stubs for frontend.
3. Implement auth and user model.
