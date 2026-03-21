# kinetic_plm

`kinetic_plm` is a Product Lifecycle Management application built on a FastAPI backend and a Vue 3 frontend. It is focused on engineering change control, product versioning, bill of materials management, approval workflows, and role-based access for engineering, approvers, operations, and admin users.

Some code and internal docs still refer to the underlying framework as `Znova`, but this repository is the Kinetic PLM application.

## What The App Covers

- Engineering Change Orders (`plm.eco`) for product and BoM changes
- Product version management (`product.version`)
- Bills of Materials and routing/work orders (`mrp.bom`, `mrp.routing.workcenter`)
- Stage-based approval flow with approver assignments
- Record comparison views for versions and BoMs
- Notifications, background jobs, audit logging, and websocket support
- Metadata-driven CRUD screens generated from backend model definitions

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL
- Frontend: Vue 3, Vite, TypeScript, Pinia, Vue Router
- Auth: JWT-based authentication with role permissions
- Realtime: WebSocket-based notifications
- Optional integrations: Google OAuth, SMTP email, Gemini-based AI impact analysis

## Repository Layout

```text
kinetic_plm/
├── backend/
│   ├── api/                    # REST endpoints
│   ├── core/                   # ORM, registry, migrations, data loader, policies
│   ├── data/                   # Core seed data: roles, stages, menus, timezones
│   ├── demo/                   # Optional demo records
│   ├── migrations/             # Alembic migrations
│   ├── models/                 # PLM domain models
│   └── services/               # Auth, email, AI, notifications
├── frontend/
│   ├── src/components/         # Shared UI components
│   ├── src/views/              # App views
│   ├── src/stores/             # Pinia stores
│   └── src/core/               # API and shared frontend utilities
├── deploy/                     # Deployment configs
├── run.py                      # Backend dev entrypoint with migration bootstrap
├── setup_fresh.py              # Recreate DB, reset migrations, optionally load demo data
├── DEVELOPMENT.md              # Framework-oriented developer notes
├── requirements.txt            # Python dependencies
└── package.json                # Root convenience scripts
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 12+

## Environment

Create a `.env` file in the project root. At minimum:

```env
DATABASE_URL=postgresql://admin:password@localhost:5432/enterprise_db
SECRET_KEY=change-this-in-real-environments
```

Useful optional variables:

```env
LOAD_DEMO_DATA=0
FRONTEND_URL=http://localhost:5173
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT=30
VITE_API_URL=http://localhost:8000/api/v1
```

Notes:

- The backend defaults `DATABASE_URL` to `postgresql://admin:password@localhost:5432/enterprise_db` if not set.
- The frontend can infer the API URL automatically, but `VITE_API_URL` is useful for non-default environments.

## Installation

### Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can also keep the virtual environment in `backend/venv`; `run.py` and `setup_fresh.py` try both locations.

### Frontend

```bash
cd frontend
npm install
cd ..
```

Or use the root helper:

```bash
npm run install:all
```

## Running The Project

### Option 1: Standard Development Start

Start the backend from the repository root:

```bash
python run.py
```

This script:

- restarts itself inside the virtualenv if one is found
- checks Alembic migration setup
- creates an initial migration if none exists
- applies migrations
- starts the FastAPI server on `http://localhost:8000`

Then start the frontend in another terminal:

```bash
cd frontend
npm run dev
```

Frontend default URL: `http://localhost:5173`

### Option 2: Fresh Database Reset

```bash
python setup_fresh.py
```

To include demo records:

```bash
python setup_fresh.py --demo
```

This reset flow:

- drops and recreates the target database
- removes old migration files in `backend/migrations/versions`
- generates a fresh initial migration
- starts the backend server
- loads core seed data, plus demo data when `--demo` is used

### Option 3: Separate Manual Start

Backend:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
npm --prefix frontend run dev
```

## Default Seeded Access

Core data creates:

- Admin: `admin@kinetic.com` / `admin123`

When demo data is enabled with `python setup_fresh.py --demo`, it also creates:

- Engineering: `engineer@kinetic.com` / `engineer123`
- Approver: `approver@kinetic.com` / `approver123`
- Operations: `ops@kinetic.com` / `ops123`

## Main Data Models

- `plm.eco`: engineering change orders, approval state, AI impact analysis, product/BoM change proposals
- `product.product`: product master record
- `product.version`: versioned product definition, pricing, attachments, linked ECO and BoM
- `mrp.bom`: bill of materials with components and routing operations
- `plm.eco.approval`: approval records for each ECO stage
- `plm.eco.stage` and `plm.eco.stage.line`: configurable workflow stages and required approvers
- `work.center`: work center master data for BoM operations

## Application Behavior

The backend uses metadata on each model to drive the frontend:

- `_role_permissions` controls role-based CRUD access and row-level domains
- `_search_config` drives list filters and groupings
- `_ui_views` defines list columns, form tabs, buttons, smart buttons, and search fields

That means many CRUD screens are generated automatically from backend model definitions rather than hand-built per entity.

## API And URLs

- Backend root: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`
- API base: `http://localhost:8000/api/v1`
- Frontend dev server: `http://localhost:5173`

Common route patterns in the UI:

- `/models/:model`
- `/models/:model/:id`
- `/comparison/:model/:id`

## Frontend Scripts

From the repository root:

```bash
npm run dev
npm run build
npm run test:frontend
```

From `frontend/`:

```bash
npm run dev
npm run build
npm run test
```

## Deployment Files

The `deploy/` directory includes:

- `Dockerfile.backend`
- `Dockerfile.frontend`
- `nginx.prod.conf`
- `render.yaml`

Review and adapt those files before using them in production.

## Current Caveats

- Some log messages and internal comments still use the framework name `Znova`.
- `setup_fresh.py` uses `fuser -k 8000/tcp 3000/tcp` during startup, which is convenient locally but should be reviewed before adapting for shared environments.
- The frontend build currently depends on the local TypeScript/Vue toolchain state; if `vue-tsc` fails in your environment, fix that separately from app code changes.

## Development Notes

- Core seed data lives in `backend/data/`
- Optional demo data lives in `backend/demo/`
- Model definitions live in `backend/models/`
- Generic UI flows are in `frontend/src/views/GenericView.vue` and shared components under `frontend/src/components/`

For framework-level implementation details, see [DEVELOPMENT.md](/home/erp/workspace/Projects/kinetic_plm/DEVELOPMENT.md).
