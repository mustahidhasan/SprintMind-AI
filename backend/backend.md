# SprintMind AI Backend + Docker Setup Guide

This document defines the backend, frontend connection, Docker setup, authentication/session flow, database setup, and local development workflow for **SprintMind AI**.

The current version must run the **frontend**, **backend**, and **PostgreSQL database** together using Docker with:

```bash
./scripts/run.sh --dev
```

The AI service is planned for later. For now, all AI-related frontend/backend operations should return **TBD** responses instead of failing.

---

## 1. Current Development Goal

The current implementation should support:

* Frontend connected with backend
* Backend API working with FastAPI
* PostgreSQL running inside Docker
* Prisma migrations for database setup
* JWT-based authentication
* Session handling through access/refresh tokens
* Protected frontend routes
* Jira connection setup using Jira base URL, email, and API token
* Jira connection test through backend
* Basic project/board sync structure
* Dashboard API responses
* Issue import/draft flow with AI operations marked as `TBD`
* Docker-based local development
* Automatic `.env` creation from `.env.example` files
* One command local startup using `./scripts/run.sh --dev`

---

## 2. Current Architecture

```text
sprintmind-ai/
│
├── frontend/
│   └── Next.js + TypeScript frontend
│
├── backend/
│   └── Python FastAPI backend
│
├── docker/
│   ├── Dockerfile.frontend
│   └── Dockerfile.backend
│
├── scripts/
│   └── run.sh
│
├── docker-compose.dev.yml
├── BACKEND.md
├── README.md
└── .gitignore
```

Current services:

```text
Frontend:   http://localhost:3000
Backend:    http://localhost:8000
PostgreSQL: localhost:5432
```

AI service is not required in the current version.

---

## 3. Current Technology Stack

### Frontend

* Next.js
* TypeScript
* Axios
* React Hook Form
* Zod
* Zustand or Context API
* TanStack Query optional

### Backend

* Python
* FastAPI
* Pydantic
* Prisma
* PostgreSQL
* JWT authentication
* Passlib/Bcrypt for password hashing
* Jira REST API integration
* Docker

### Database

* PostgreSQL inside Docker for local development
* AWS RDS PostgreSQL will be added later
* Cloudflare D1 is not used in the current version

---

## 4. Backend Responsibilities

The backend must handle:

* User registration
* User login
* JWT access token generation
* Refresh token generation
* Session validation
* Protected API routes
* User profile endpoint
* Jira connection storage
* Jira token encryption before saving
* Jira connection testing
* Jira project/board/sprint sync API structure
* Basic dashboard data
* Issue import/draft data storage
* AI placeholder responses
* Audit logs for important actions

---

## 5. Frontend Responsibilities

The frontend must handle:

* Register page
* Login page
* Logout
* Protected routes
* Auth session persistence
* Dashboard page
* Jira connection page
* Jira project/board selection page
* Issue import page
* Issue drafts page
* Approval page
* Settings page
* API calls using Axios
* Token refresh flow
* Redirect unauthenticated users to login
* Redirect new users to Jira onboarding

---

## 6. API Prefix Rule

All backend API routes must use:

```text
/api/v1
```

Example:

```text
/api/v1/auth/login
/api/v1/jira/connect
/api/v1/issues/import
```

---

## 7. Backend Folder Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── jwt.py
│   │   ├── encryption.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       ├── health.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── jira.py
│   │       ├── dashboard.py
│   │       ├── issues.py
│   │       ├── approvals.py
│   │       └── ai_placeholder.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── jira.py
│   │   ├── issue.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── jira_service.py
│   │   ├── dashboard_service.py
│   │   ├── issue_service.py
│   │   ├── approval_service.py
│   │   └── audit_service.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── db.py
│   │
│   └── prisma_client.py
│
├── prisma/
│   └── schema.prisma
│
├── scripts/
│   ├── init_db.py
│   ├── seed_dev_data.py
│   └── check_env.py
│
├── requirements.txt
├── pyproject.toml
├── .env.dev.example
├── .env.prod.example
└── README.md
```

---

## 8. Frontend Folder Structure

```text
frontend/
│
├── src/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   │
│   │   ├── auth/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   │
│   │   ├── dashboard/page.tsx
│   │   │
│   │   ├── onboarding/
│   │   │   ├── page.tsx
│   │   │   ├── connect-jira/page.tsx
│   │   │   └── select-project/page.tsx
│   │   │
│   │   ├── jira/
│   │   │   ├── connection/page.tsx
│   │   │   ├── projects/page.tsx
│   │   │   └── boards/page.tsx
│   │   │
│   │   ├── issues/
│   │   │   ├── page.tsx
│   │   │   ├── import/page.tsx
│   │   │   ├── drafts/page.tsx
│   │   │   └── [issueId]/page.tsx
│   │   │
│   │   ├── approvals/page.tsx
│   │   └── settings/page.tsx
│   │
│   ├── components/
│   ├── features/
│   ├── hooks/
│   ├── lib/
│   │   ├── axios.ts
│   │   └── auth.ts
│   ├── stores/
│   └── types/
│
├── .env.dev.example
├── .env.prod.example
├── package.json
└── next.config.ts
```

---

## 9. Authentication Requirement

Use JWT authentication.

The backend should issue:

* Access token
* Refresh token

Recommended token behavior:

```text
Access token expiry: 15 minutes
Refresh token expiry: 7 days
```

The frontend should store the access token safely and use it for API calls.

Recommended frontend handling:

* Store access token in memory or secure app state
* Store refresh token in HTTP-only cookie if implemented
* If HTTP-only cookie is not implemented yet, store refresh token carefully for local development only
* On 401 response, call refresh endpoint
* If refresh fails, logout user

---

## 10. Auth API Routes

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

### Register Request

```json
{
  "name": "Mustahid Hasan",
  "email": "mustahid@example.com",
  "password": "StrongPassword123"
}
```

### Register Response

```json
{
  "success": true,
  "message": "Registration successful",
  "data": {
    "user": {
      "id": "user_id",
      "name": "Mustahid Hasan",
      "email": "mustahid@example.com"
    },
    "accessToken": "jwt_access_token",
    "refreshToken": "jwt_refresh_token"
  }
}
```

### Login Request

```json
{
  "email": "mustahid@example.com",
  "password": "StrongPassword123"
}
```

### Login Response

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "user_id",
      "name": "Mustahid Hasan",
      "email": "mustahid@example.com"
    },
    "accessToken": "jwt_access_token",
    "refreshToken": "jwt_refresh_token"
  }
}
```

### Me Response

```json
{
  "success": true,
  "data": {
    "id": "user_id",
    "name": "Mustahid Hasan",
    "email": "mustahid@example.com",
    "hasJiraConnection": true
  }
}
```

---

## 11. Frontend Auth Flow

```text
User opens app
        ↓
Check local auth/session state
        ↓
Call /api/v1/auth/me if token exists
        ↓
If valid → dashboard or onboarding
        ↓
If invalid → login
```

After login:

```text
If user has Jira connection:
    redirect to /dashboard

If user has no Jira connection:
    redirect to /onboarding/connect-jira
```

Protected pages:

```text
/dashboard
/onboarding/*
/jira/*
/issues/*
/approvals
/settings
```

Public pages:

```text
/
/auth/login
/auth/register
```

---

## 12. Axios Setup

Frontend must use Axios for backend communication.

File:

```text
frontend/src/lib/axios.ts
```

Required behavior:

* Base URL from environment
* Attach access token to requests
* Handle 401 responses
* Refresh token when possible
* Logout if refresh fails

Example base URL:

```env
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000/api/v1
```

---

## 13. Jira Connection Flow

The current version must allow users to connect Jira using:

* Jira base URL
* Jira email
* Jira API token
* Connection name

Example Jira base URL:

```text
https://your-company.atlassian.net
```

The API token must never be exposed in frontend responses.

The backend must encrypt the Jira API token before saving it.

---

## 14. Jira API Routes

```text
POST   /api/v1/jira/connect
POST   /api/v1/jira/test-connection
GET    /api/v1/jira/connection
DELETE /api/v1/jira/connection
POST   /api/v1/jira/sync
GET    /api/v1/jira/projects
GET    /api/v1/jira/boards
GET    /api/v1/jira/sprints
```

### Connect Jira Request

```json
{
  "connectionName": "My Jira Workspace",
  "baseUrl": "https://your-company.atlassian.net",
  "email": "user@company.com",
  "apiToken": "jira_api_token"
}
```

### Connect Jira Response

```json
{
  "success": true,
  "message": "Jira connected successfully",
  "data": {
    "id": "connection_id",
    "connectionName": "My Jira Workspace",
    "baseUrl": "https://your-company.atlassian.net",
    "email": "user@company.com",
    "status": "CONNECTED"
  }
}
```

### Test Jira Connection Response

```json
{
  "success": true,
  "message": "Jira connection is valid",
  "data": {
    "status": "CONNECTED",
    "accountName": "User Name",
    "accountEmail": "user@company.com"
  }
}
```

---

## 15. Jira Frontend Flow

```text
User goes to /onboarding/connect-jira
        ↓
User enters base URL, email, API token
        ↓
Frontend calls /api/v1/jira/test-connection
        ↓
If valid, user clicks Save Connection
        ↓
Frontend calls /api/v1/jira/connect
        ↓
Backend encrypts and saves token
        ↓
User goes to /onboarding/select-project
        ↓
Frontend fetches projects and boards
        ↓
User selects default project and board
        ↓
User goes to /dashboard
```

---

## 16. Dashboard API

```text
GET /api/v1/dashboard/summary
```

Response:

```json
{
  "success": true,
  "data": {
    "totalIssues": 0,
    "highRiskIssues": 0,
    "averageQualityScore": 0,
    "pendingApprovals": 0,
    "sprintRisk": "TBD",
    "businessImpact": "TBD",
    "aiStatus": "TBD"
  }
}
```

Current AI-related dashboard values should show:

```text
TBD
```

---

## 17. Issue Import Flow

The frontend should support:

* Manual issue input
* CSV upload UI placeholder
* Existing Jira issue sync placeholder

Current working scope:

* Manual issue input should work
* Backend should save imported issue draft
* AI analysis should return `TBD`

---

## 18. Issue API Routes

```text
GET  /api/v1/issues
POST /api/v1/issues/import
GET  /api/v1/issues/drafts
GET  /api/v1/issues/{issue_id}
POST /api/v1/issues/{issue_id}/send-to-approval
```

### Import Issue Request

```json
{
  "title": "Build login page",
  "description": "Create login page with email and password",
  "sourceType": "MANUAL",
  "priority": "MEDIUM"
}
```

### Import Issue Response

```json
{
  "success": true,
  "message": "Issue draft created",
  "data": {
    "id": "issue_id",
    "title": "Build login page",
    "description": "Create login page with email and password",
    "sourceType": "MANUAL",
    "status": "DRAFT",
    "aiStatus": "TBD"
  }
}
```

---

## 19. AI Placeholder Routes

AI operations are not implemented in the current version.

The backend should expose placeholder routes so the frontend does not break.

```text
POST /api/v1/ai/issue/generate
POST /api/v1/ai/issue/quality-score
POST /api/v1/ai/sprint/risk-score
POST /api/v1/ai/business/impact-score
```

Placeholder response:

```json
{
  "success": true,
  "message": "AI operation is TBD",
  "data": {
    "status": "TBD"
  }
}
```

Frontend should display:

```text
AI operation: TBD
```

---

## 20. Approval Flow

Current approval flow should work as a backend/frontend feature even if AI is TBD.

Approval actions:

* Send issue draft to approval
* Approve issue draft
* Reject issue draft

Creating the actual Jira issue can be implemented after the basic flow is working.

---

## 21. Approval API Routes

```text
GET  /api/v1/approvals
POST /api/v1/approvals/{approval_id}/approve
POST /api/v1/approvals/{approval_id}/reject
```

Approval statuses:

```text
PENDING
APPROVED
REJECTED
APPLIED_TO_JIRA
```

---

## 22. Prisma Requirement

Use Prisma for all database schema and migrations.

Do not use raw SQL setup as the primary setup.

Required commands:

```bash
cd backend
prisma generate
prisma migrate dev
prisma migrate deploy
```

In Docker, these commands should be executed inside the backend container.

---

## 23. Initial Prisma Models

The current version should include these models:

```text
User
RefreshToken
JiraConnection
Project
Board
Sprint
IssueDraft
ApprovalRequest
AuditLog
```

---

## 24. Prisma Schema Requirements

### User

Fields:

```text
id
name
email
passwordHash
createdAt
updatedAt
```

### RefreshToken

Fields:

```text
id
userId
tokenHash
expiresAt
revokedAt
createdAt
```

### JiraConnection

Fields:

```text
id
userId
connectionName
baseUrl
email
encryptedApiToken
status
lastTestedAt
createdAt
updatedAt
```

### Project

Fields:

```text
id
userId
jiraConnectionId
jiraProjectId
key
name
createdAt
updatedAt
```

### Board

Fields:

```text
id
userId
jiraConnectionId
jiraBoardId
name
type
createdAt
updatedAt
```

### Sprint

Fields:

```text
id
userId
boardId
jiraSprintId
name
state
startDate
endDate
createdAt
updatedAt
```

### IssueDraft

Fields:

```text
id
userId
title
description
sourceType
priority
status
aiStatus
jiraIssueKey
createdAt
updatedAt
```

### ApprovalRequest

Fields:

```text
id
userId
issueDraftId
type
status
createdAt
updatedAt
```

### AuditLog

Fields:

```text
id
userId
action
entityType
entityId
metadata
createdAt
```

---

## 25. Environment Files

The app must have local environment examples.

```text
frontend/.env.dev.example
backend/.env.dev.example
```

The `run.sh --dev` command must generate local `.env.dev` files from examples if they do not exist.

---

## 26. Frontend Environment Example

File:

```text
frontend/.env.dev.example
```

Content:

```env
NODE_ENV=development
NEXT_PUBLIC_APP_NAME=SprintMind AI
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 27. Backend Environment Example

File:

```text
backend/.env.dev.example
```

Content:

```env
APP_ENV=development
APP_NAME=SprintMind AI Backend
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/sprintmind_dev

FRONTEND_URL=http://localhost:3000

JWT_SECRET=change_me_dev_jwt_secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

ENCRYPTION_KEY=change_me_32_char_encryption_key

LOG_LEVEL=debug
```

---

## 28. Docker Requirements

The current Docker setup must include:

```text
docker/Dockerfile.frontend
docker/Dockerfile.backend
docker-compose.dev.yml
scripts/run.sh
```

The AI container is not required in the current version.

---

## 29. Docker Compose Development Setup

File:

```text
docker-compose.dev.yml
```

Services:

```text
frontend
backend
postgres
```

Ports:

```text
frontend: 3000
backend: 8000
postgres: 5432
```

Required behavior:

* Frontend depends on backend
* Backend depends on postgres
* PostgreSQL data must persist using Docker volume
* Backend must run migrations on startup or through `run.sh`
* Frontend must connect to backend using `NEXT_PUBLIC_BACKEND_API_URL`

---

## 30. Docker Compose Development Specification

```yaml
services:
  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    env_file:
      - frontend/.env.dev
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    env_file:
      - backend/.env.dev
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: sprintmind_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - sprintmind_postgres_data:/var/lib/postgresql/data

volumes:
  sprintmind_postgres_data:
```

---

## 31. Dockerfile Frontend Requirement

File:

```text
docker/Dockerfile.frontend
```

Must:

* Use Node LTS
* Install dependencies
* Run Next.js dev server in development
* Expose port 3000

Development command should run:

```bash
npm run dev
```

---

## 32. Dockerfile Backend Requirement

File:

```text
docker/Dockerfile.backend
```

Must:

* Use Python 3.11 or 3.12
* Install backend dependencies
* Install Prisma CLI/client requirements
* Expose port 8000
* Run FastAPI using Uvicorn

Development command should run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 33. run.sh Requirement

File:

```text
scripts/run.sh
```

Command:

```bash
./scripts/run.sh --dev
```

Expected behavior:

1. Check that Docker is installed
2. Check that Docker Compose is available
3. Create `frontend/.env.dev` from `frontend/.env.dev.example` if missing
4. Create `backend/.env.dev` from `backend/.env.dev.example` if missing
5. Build Docker images
6. Start PostgreSQL
7. Wait for PostgreSQL to be ready
8. Start backend
9. Run Prisma generate
10. Run Prisma migration
11. Start frontend
12. Print service URLs

Output:

```text
SprintMind AI is running

Frontend: http://localhost:3000
Backend:  http://localhost:8000
Postgres: localhost:5432
```

---

## 34. Local Development Command

The only required command for local development should be:

```bash
./scripts/run.sh --dev
```

If permission is missing:

```bash
chmod +x scripts/run.sh
./scripts/run.sh --dev
```

---

## 35. Health Check Routes

Backend health route:

```text
GET /api/v1/health
```

Response:

```json
{
  "success": true,
  "message": "SprintMind AI backend is running",
  "data": {
    "status": "ok",
    "service": "backend"
  }
}
```

Frontend should call this route to confirm backend connection.

---

## 36. Frontend Pages Required in Current Version

The current frontend must include:

```text
/
/auth/login
/auth/register
/dashboard
/onboarding/connect-jira
/onboarding/select-project
/jira/connection
/issues
/issues/import
/issues/drafts
/approvals
/settings
```

AI-heavy pages can show `TBD`.

---

## 37. Current Working Features

The current version must support:

### Auth

* Register user
* Login user
* Logout user
* Refresh session/token
* Get current user
* Protect routes

### Jira

* Save Jira connection
* Test Jira connection
* Show connection status
* Delete Jira connection
* Placeholder project/board/sprint sync if real Jira sync is not complete

### Issues

* Create issue draft manually
* List issue drafts
* View issue draft
* Send issue draft to approval

### Approvals

* List approvals
* Approve issue draft
* Reject issue draft

### Dashboard

* Show basic summary
* Show Jira connection status
* Show issue draft count
* Show approval count
* Show AI fields as `TBD`

---

## 38. Features That Should Show TBD for Now

The following should not break the app, but should show `TBD`:

```text
AI issue generation
Issue quality scoring
Sprint risk prediction
Business impact scoring
Duplicate detection
LLM recommendation engine
AI explanation engine
```

Example UI message:

```text
This AI feature is planned and will be implemented in the next phase.
Status: TBD
```

---

## 39. Error Handling

Backend should return consistent error responses.

Example:

```json
{
  "success": false,
  "message": "Invalid credentials",
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS"
  }
}
```

Frontend should show:

* Toast messages
* Form validation errors
* Loading states
* Empty states
* API error messages

---

## 40. Security Requirements

The current version must include:

* Password hashing
* JWT authentication
* Refresh token support
* Protected routes
* Encrypted Jira API token
* No secrets in frontend
* No secrets in logs
* `.env` files ignored by Git
* CORS configured only for frontend URL
* Basic audit logs

---

## 41. CORS Requirement

Backend must allow frontend origin.

Development:

```text
http://localhost:3000
```

Backend CORS should use `FRONTEND_URL` from environment.

---

## 42. Git Ignore Requirements

The project `.gitignore` must include:

```gitignore
.env
.env.*
!.env.example
!.env.dev.example
!.env.prod.example

__pycache__/
*.py[cod]
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/

node_modules/
.next/
out/
dist/
build/

*.sqlite3
*.db

data/raw/
data/private/
uploads/
outputs/

logs/
*.log

.vscode/
.idea/
.DS_Store

docker-compose.override.yml
```

---

## 43. Final Local MVP Definition

The local MVP is complete when:

```text
./scripts/run.sh --dev
```

successfully starts:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
Postgres: localhost:5432
```

And the user can:

1. Register
2. Login
3. Stay authenticated using session/token
4. Open protected dashboard
5. Connect Jira using base URL, email, and API token
6. Test Jira connection
7. Create manual issue draft
8. View issue drafts
9. Send issue draft to approval
10. Approve or reject issue draft
11. See AI features as `TBD`
12. Logout

---

## 44. Current Phase Summary

This phase is not focused on AI model implementation yet.

This phase is focused on:

* Correct full-stack connection
* Working authentication
* PostgreSQL database in Docker
* Prisma migrations
* Jira connection flow
* Frontend/backend integration
* Docker-based local development
* Stable app foundation

AI will be implemented in the next phase.
