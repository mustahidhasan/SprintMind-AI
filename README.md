# SprintMind AI

**SprintMind AI** is an LLM-powered Jira workflow automation and sprint risk intelligence platform for agile software teams.

It converts raw requirements, meeting notes, CSV tasks, and Google Sheet entries into structured Jira issues. It also improves issue quality, predicts sprint delivery risks, estimates business impact, and gives explainable recommendations before delivery problems happen.

---

## Project Purpose

SprintMind AI is designed as a research-ready and production-style platform for AI-assisted agile project management.

The system focuses on:

* Jira issue automation
* Workflow automation
* LLM-based requirement understanding
* Sprint risk prediction
* Issue quality scoring
* Business impact analysis
* Human-approved Jira updates
* Explainable AI recommendations

This project is also designed for portfolio, research, and PhD/HDR funding preparation in the area of **AI for Software Engineering**.

---

## Research Direction

### Research Title

**SprintMind AI: LLM-Powered Jira Automation and Sprint Risk Intelligence Platform**

### Research Area

* AI for Software Engineering
* LLM-assisted Agile Project Management
* Workflow Automation
* Jira Issue Analytics
* Sprint Risk Prediction
* Software Project Intelligence
* Human-in-the-loop Automation

### Problem Statement

Agile teams create many Jira issues, sprint updates, comments, and requirements every day. Many of these tickets are incomplete, unclear, duplicated, or poorly prioritized.

This causes:

* Sprint delays
* Rework
* Poor requirement clarity
* Manual project management effort
* Missed blockers
* Wrong task priority
* Weak business visibility

SprintMind AI solves this by using LLMs, software analytics, and automation to improve Jira workflows and predict delivery risks.

---

## Core Features

### 1. Requirement to Jira Pipeline

SprintMind AI converts raw project inputs into structured Jira issues.

Supported inputs:

* CSV files
* Google Sheets
* Meeting notes
* Requirement documents
* Manual task input
* Existing Jira issue data

Generated Jira fields:

* Title
* Description
* Acceptance criteria
* Issue type
* Priority
* Labels
* Components
* Suggested sprint
* Suggested assignee
* Dependencies

---

### 2. LLM Issue Builder

The AI service uses LLMs to improve raw requirements.

It can:

* Rewrite unclear requirements
* Generate acceptance criteria
* Classify issue type
* Suggest priority
* Suggest labels
* Detect missing information
* Split large tasks into smaller tasks
* Normalize task descriptions

---

### 3. Issue Quality Scoring

Each issue receives a quality score.

Quality is measured using:

* Requirement clarity
* Completeness
* Testability
* Acceptance criteria quality
* Dependency clarity
* Business value clarity
* Technical scope clarity

Example:

```text
Issue Quality Score: 68/100

Problems:
- Acceptance criteria missing
- Requirement is too broad
- Priority is unclear

Recommendation:
- Add acceptance criteria
- Split into frontend, backend, and QA tasks
- Confirm expected business outcome
```

---

### 4. Sprint Risk Prediction

The system predicts delivery risks before they become problems.

Risk prediction includes:

* Issue delay risk
* Sprint overload risk
* Reopen probability
* Blocker probability
* Cycle-time estimate
* Delivery confidence score
* Release delay risk

Possible prediction factors:

* Issue type
* Priority
* Labels
* Description length
* Comment count
* Status movement
* Assignee workload
* Sprint capacity
* Historical cycle time
* Similar issue history

---

### 5. Business Impact Engine

This module adds business value to the project.

It can estimate:

* Cost of delay
* Release risk
* Customer impact
* Business priority alignment
* Sprint commitment risk
* Planning effort reduction
* Rework reduction

Example:

```text
Business Impact: High

Reason:
- The issue is linked to a release-critical module
- Similar issues delayed previous sprints
- Sprint capacity is already overloaded

Recommended Action:
- Assign senior reviewer
- Reduce sprint scope
- Split issue into smaller tasks
```

---

### 6. Human Approval Workflow

SprintMind AI should not directly update Jira without approval.

Workflow:

1. AI analyzes the task or sprint data
2. AI suggests issue creation or update
3. PM or team lead reviews the suggestion
4. User approves or rejects the suggestion
5. Backend updates Jira through Jira REST API
6. System stores audit logs

This makes the system safer for real business use.

---

## Technology Stack

### Frontend

* Next.js
* TypeScript
* Axios
* Cloudflare Pages

### Backend

* Python
* FastAPI
* Prisma
* PostgreSQL
* Jira REST API
* Google Sheets API
* Cloudflare Container

### AI Service

* Python
* FastAPI
* LLM API
* Pandas
* scikit-learn
* Transformers or embeddings
* Cloudflare Container

### Database

* PostgreSQL for local development
* AWS RDS PostgreSQL for production
* Cloudflare D1 will not be used in the current version
* Cloudflare D1 may be explored later as a future optional metadata layer

### DevOps

* Docker
* Docker Compose
* Cloudflare Pages
* Cloudflare Workers / Containers
* Shell scripts

---

## Project Structure

```text
sprintmind-ai/
│
├── frontend/
│   └── Next.js + TypeScript frontend
│
├── backend/
│   └── Python FastAPI backend
│
├── ai/
│   └── Python FastAPI AI service
│
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── Dockerfile.ai
│
├── scripts/
│   ├── run.sh
│   └── deploy.sh
│
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── README.md
├── LICENSE
└── .gitignore
```

---

## Service Architecture

### Frontend Service

The frontend is responsible for:

* Dashboard UI
* Issue analysis view
* Sprint risk dashboard
* Approval workflow screen
* Business impact report
* Settings page
* Jira connection UI

Local URL:

```text
http://localhost:3000
```

---

### Backend Service

The backend is the main API layer.

It is responsible for:

* Authentication
* Jira API integration
* Google Sheets integration
* Project and sprint management
* Approval workflow
* Prisma database access
* Audit logging
* Report generation
* Communication with AI service

Local URL:

```text
http://localhost:8000
```

API prefix:

```text
/api/v1
```

---

### AI Service

The AI service handles all LLM and prediction-related tasks.

It is responsible for:

* Issue generation
* Acceptance criteria generation
* Issue classification
* Quality scoring
* Duplicate detection
* Sprint risk prediction
* Business impact scoring
* Explainable recommendations

Local URL:

```text
http://localhost:8777
```

API prefix:

```text
/api/v1
```

---

## API Route Rules

All backend and AI routes must use:

```text
/api/v1
```

Example backend routes:

```text
GET    /api/v1/health
POST   /api/v1/auth/login
POST   /api/v1/jira/connect
POST   /api/v1/issues/analyze
POST   /api/v1/issues/create-draft
POST   /api/v1/issues/approve
POST   /api/v1/sprints/risk
GET    /api/v1/reports/sprint-health
```

Example AI routes:

```text
GET    /api/v1/health
POST   /api/v1/issue/generate
POST   /api/v1/issue/quality-score
POST   /api/v1/issue/duplicate-check
POST   /api/v1/sprint/risk-score
POST   /api/v1/business/impact-score
POST   /api/v1/explain
```

---

## Frontend Communication

The frontend must use Axios to communicate with the backend.

```ts
import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_API_URL,
  timeout: 30000,
});
```

Development backend URL:

```env
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000/api/v1
```

---

## Backend to AI Communication

The backend communicates with the AI service through internal Docker networking.

Internal AI service URL:

```env
AI_SERVICE_URL=http://ai:8777/api/v1
```

The AI service should not be publicly exposed unless required.

---

## Database Strategy

The project must use **Prisma** for schema management, migrations, and database client generation.

Raw SQL should not be used as the main database setup method.

### Development Database

Development uses PostgreSQL.

Supported options:

* Local PostgreSQL container
* Remote development AWS RDS PostgreSQL

### Production Database

Production uses:

```text
AWS RDS PostgreSQL
```

Current version will not use Cloudflare D1.

Reason:

* The backend is Python FastAPI
* The project needs relational models
* Prisma migrations are required
* Sprint, issue, project, analytics, audit, and experiment data are better handled in PostgreSQL
* Cloudflare D1 is SQLite-based and will be explored later only if needed

---

## Suggested Database Entities

Recommended entities:

```text
User
Organization
Project
JiraConnection
Sprint
Issue
IssueAnalysis
IssueQualityScore
RiskPrediction
BusinessImpactScore
AIRecommendation
ApprovalRequest
AutomationLog
Dataset
ExperimentRun
ModelMetric
AuditLog
```

---

## Environment Files

Each service must have separate development and production environment examples.

Total environment example files:

```text
frontend/.env.dev.example
frontend/.env.prod.example

backend/.env.dev.example
backend/.env.prod.example

ai/.env.dev.example
ai/.env.prod.example
```

---

## Frontend Environment

### frontend/.env.dev.example

```env
NODE_ENV=development
NEXT_PUBLIC_APP_NAME=SprintMind AI
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### frontend/.env.prod.example

```env
NODE_ENV=production
NEXT_PUBLIC_APP_NAME=SprintMind AI
NEXT_PUBLIC_BACKEND_API_URL=https://api.your-domain.com/api/v1
NEXT_PUBLIC_APP_URL=https://your-domain.com
```

---

## Backend Environment

### backend/.env.dev.example

```env
APP_ENV=development
APP_NAME=SprintMind AI Backend
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/sprintmind_dev

AI_SERVICE_URL=http://ai:8777/api/v1
FRONTEND_URL=http://localhost:3000

JWT_SECRET=change_me_dev_jwt_secret
ENCRYPTION_KEY=change_me_32_char_encryption_key

JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_SHEETS_API_KEY=

LOG_LEVEL=debug
```

### backend/.env.prod.example

```env
APP_ENV=production
APP_NAME=SprintMind AI Backend
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql://USER:PASSWORD@YOUR_RDS_HOST:5432/sprintmind_prod

AI_SERVICE_URL=http://ai:8777/api/v1
FRONTEND_URL=https://your-domain.com

JWT_SECRET=
ENCRYPTION_KEY=

JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_SHEETS_API_KEY=

LOG_LEVEL=info
```

---

## AI Environment

### ai/.env.dev.example

```env
APP_ENV=development
APP_NAME=SprintMind AI Service
APP_HOST=0.0.0.0
APP_PORT=8777

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=

MODEL_PROVIDER=openai
LLM_MODEL_NAME=gpt-4o-mini
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

BACKEND_INTERNAL_API_URL=http://backend:8000/api/v1

LOG_LEVEL=debug
```

### ai/.env.prod.example

```env
APP_ENV=production
APP_NAME=SprintMind AI Service
APP_HOST=0.0.0.0
APP_PORT=8777

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=

MODEL_PROVIDER=openai
LLM_MODEL_NAME=
EMBEDDING_MODEL_NAME=

BACKEND_INTERNAL_API_URL=http://backend:8000/api/v1

LOG_LEVEL=info
```

---

## Docker Setup

The project must include separate Dockerfiles for each service.

```text
docker/Dockerfile.frontend
docker/Dockerfile.backend
docker/Dockerfile.ai
```

The project must include two Docker Compose files.

```text
docker-compose.dev.yml
docker-compose.prod.yml
```

---

## Development Docker Compose

`docker-compose.dev.yml` should run:

* Frontend on port `3000`
* Backend on port `8000`
* AI service on port `8777`
* PostgreSQL on port `5432`

Development command:

```bash
./scripts/run.sh --dev
```

Expected local URLs:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
AI:       http://localhost:8777
```

---

## Production Docker Compose

`docker-compose.prod.yml` should run:

* Frontend service if needed
* Backend service
* AI service

Production should connect to external AWS RDS PostgreSQL.

Production command:

```bash
./scripts/run.sh --prod
```

---

## Scripts

All main scripts should be placed inside:

```text
scripts/
```

Required scripts:

```text
scripts/run.sh
scripts/deploy.sh
```

Both scripts must support:

```bash
--dev
--prod
```

---

## run.sh Requirement

### Development

Command:

```bash
./scripts/run.sh --dev
```

Expected behavior:

* Validate required folders
* Create env files from examples if missing
* Install frontend dependencies
* Install backend dependencies
* Install AI dependencies
* Start Docker Compose development stack
* Run Prisma generate
* Run Prisma migrations
* Start all services

### Production

Command:

```bash
./scripts/run.sh --prod
```

Expected behavior:

* Validate production env files
* Build production Docker images
* Run Prisma production migration
* Start production stack
* Check health endpoints

---

## deploy.sh Requirement

### Development

Command:

```bash
./scripts/deploy.sh --dev
```

Expected behavior:

* Build dev images
* Run dev stack
* Check service health

### Production

Command:

```bash
./scripts/deploy.sh --prod
```

Expected behavior:

* Validate production secrets
* Build production images
* Run tests
* Run Prisma production migration
* Build frontend
* Deploy frontend to Cloudflare Pages
* Deploy backend to Cloudflare Worker or Container
* Deploy AI service to Cloudflare Container
* Verify health endpoints

---

## Backend Helper Scripts

Backend helper scripts should be placed in:

```text
backend/scripts/
```

Recommended scripts:

```text
init_db.py
seed_dev_data.py
sync_jira_sample.py
generate_report.py
check_env.py
```

---

## AI Helper Scripts

AI helper scripts should be placed in:

```text
ai/scripts/
```

Recommended scripts:

```text
run_quality_eval.py
train_delay_model.py
evaluate_predictions.py
build_embeddings.py
test_llm_prompts.py
export_metrics.py
```

---

## Frontend Folder Routing

Use Next.js folder-based routing.

Recommended structure:

```text
frontend/src/app/
│
├── page.tsx
├── layout.tsx
│
├── dashboard/
│   └── page.tsx
│
├── projects/
│   ├── page.tsx
│   └── [projectId]/
│       └── page.tsx
│
├── issues/
│   ├── page.tsx
│   └── [issueId]/
│       └── page.tsx
│
├── sprints/
│   ├── page.tsx
│   └── [sprintId]/
│       └── page.tsx
│
├── recommendations/
│   └── page.tsx
│
├── approvals/
│   └── page.tsx
│
└── settings/
    └── page.tsx
```

---

## Backend Folder Structure

```text
backend/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       ├── auth.py
│   │       ├── jira.py
│   │       ├── issues.py
│   │       ├── sprints.py
│   │       ├── recommendations.py
│   │       ├── approvals.py
│   │       └── reports.py
│   │
│   ├── services/
│   │   ├── jira_service.py
│   │   ├── ai_client.py
│   │   ├── approval_service.py
│   │   ├── report_service.py
│   │   └── audit_service.py
│   │
│   ├── schemas/
│   │   ├── issue.py
│   │   ├── sprint.py
│   │   ├── recommendation.py
│   │   └── approval.py
│   │
│   └── prisma_client.py
│
├── prisma/
│   └── schema.prisma
│
├── scripts/
├── requirements.txt
├── pyproject.toml
├── .env.dev.example
└── .env.prod.example
```

---

## AI Folder Structure

```text
ai/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       ├── issue_generation.py
│   │       ├── quality_score.py
│   │       ├── duplicate_check.py
│   │       ├── sprint_risk.py
│   │       ├── business_impact.py
│   │       └── explainability.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── prompt_service.py
│   │   ├── quality_service.py
│   │   ├── prediction_service.py
│   │   ├── business_impact_service.py
│   │   └── explanation_service.py
│   │
│   ├── models/
│   │   ├── delay_model.py
│   │   ├── sprint_risk_model.py
│   │   └── duplicate_model.py
│   │
│   └── schemas/
│       ├── issue.py
│       ├── risk.py
│       └── recommendation.py
│
├── scripts/
├── notebooks/
├── datasets/
├── requirements.txt
├── pyproject.toml
├── .env.dev.example
└── .env.prod.example
```

---

## Cloudflare Deployment Plan

Target deployment:

```text
Frontend:
Cloudflare Pages

Backend:
Cloudflare Worker or Cloudflare Container

AI:
Cloudflare Container

Database:
AWS RDS PostgreSQL

Docker:
Used for local development and container-based service management
```

Important note:

Cloudflare Pages and Workers do not run Docker Compose directly like a VPS. Docker Compose is mainly for local development or server-style deployment. For Cloudflare production, each service may need its own Cloudflare deployment configuration.

Cloudflare D1 is not part of the current architecture.

---

## Security Requirements

The project must include:

* No hardcoded secrets
* Environment-based configuration
* Encrypted Jira API tokens
* Role-based access control
* Audit logs
* Human approval before Jira updates
* Safe logging without secrets
* Private data anonymization

---

## Privacy Requirements

Do not expose private company data.

Use:

* Public Jira datasets
* Public GitHub issue datasets
* Synthetic sprint data
* Demo Jira workspace
* Anonymized samples

Before using real data, remove:

* Names
* Emails
* Client identifiers
* Project names
* Internal URLs
* Confidential comments

---

## Research Deliverables

The project should produce:

* Working MVP
* GitHub repository
* Architecture diagram
* Demo video
* 1-page professor proposal
* 4-6 page mini research report
* Dataset plan
* Model evaluation table
* Screenshots
* Deployment documentation

---

## Evaluation Metrics

### AI Metrics

* Accuracy
* Precision
* Recall
* F1-score
* AUC
* MAE for cycle-time prediction

### Product Metrics

* Time saved per Jira ticket
* Reduction in missing acceptance criteria
* Reduction in unclear requirements
* Reopened issue prediction accuracy
* Sprint risk prediction accuracy
* PM usefulness score
* Developer usefulness score

### Business Metrics

* Estimated cost of delay
* Sprint overload detection
* Release risk reduction
* Planning effort reduction
* Rework reduction

---

## MVP Scope

The first complete MVP should include:

* Frontend dashboard
* Backend FastAPI service
* AI FastAPI service
* Jira API integration
* CSV task upload
* AI issue generation
* Issue quality scoring
* Sprint risk scoring
* Business impact scoring
* Human approval screen
* Prisma schema and migrations
* PostgreSQL development database
* AWS RDS PostgreSQL production database
* Docker Compose dev and prod files
* run.sh and deploy.sh
* README and documentation

---

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sprintmind-ai.git
cd sprintmind-ai
```

### 2. Create environment files

```bash
cp frontend/.env.dev.example frontend/.env.dev
cp backend/.env.dev.example backend/.env.dev
cp ai/.env.dev.example ai/.env.dev
```

### 3. Start development stack

```bash
chmod +x scripts/run.sh
./scripts/run.sh --dev
```

Expected URLs:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
AI:       http://localhost:8777
```

---

## Production Setup

### 1. Create production environment files

```bash
cp frontend/.env.prod.example frontend/.env.prod
cp backend/.env.prod.example backend/.env.prod
cp ai/.env.prod.example ai/.env.prod
```

### 2. Fill required secrets

Required values:

```text
DATABASE_URL
JWT_SECRET
ENCRYPTION_KEY
JIRA_BASE_URL
JIRA_EMAIL
JIRA_API_TOKEN
OPENAI_API_KEY or another LLM provider key
```

### 3. Run production stack

```bash
chmod +x scripts/run.sh
./scripts/run.sh --prod
```

### 4. Deploy production

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh --prod
```

---

## Git Ignore Requirements

Recommended ignored files:

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

## License

Recommended license:

```text
MIT License
```

---

## Professor / Research Pitch

SprintMind AI is a research-based AI for Software Engineering project focused on LLM-assisted Jira workflow automation and sprint risk intelligence. The system converts unstructured requirements into high-quality Jira issues, detects missing acceptance criteria and unclear requirements, predicts issue and sprint delivery risks, explains risk factors, estimates business impact, and supports human-approved workflow automation.

The research goal is to study how LLMs and software analytics can improve agile project management, developer productivity, and delivery reliability.

---

## Future Plan

Cloudflare D1 is not used in the current version.

Later, D1 may be explored for:

* Lightweight metadata storage
* Edge-friendly configuration
* Read-heavy public dashboard data
* Cloudflare-native modules

For now, the main production database is:

```text
AWS RDS PostgreSQL
```

---

## Final Target

By the end of the first project phase, SprintMind AI should be ready for:

* GitHub portfolio
* Professor outreach
* PhD/HDR proposal support
* Research mini-paper
* Demo presentation
* Future SaaS or Jira Marketplace extension
