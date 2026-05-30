# SprintMind AI - AI Service Implementation Guide

This document defines the complete AI service implementation plan for **SprintMind AI**.

The frontend and backend are already connected and running through Docker. This phase adds the dedicated **AI service** as a separate Python FastAPI microservice.

The AI service will handle:

* LLM-powered Jira issue generation
* Acceptance criteria generation
* Issue type classification
* Priority and label suggestion
* Issue quality scoring
* Duplicate/similar issue detection
* Sprint risk prediction
* Business impact scoring
* Explainable recommendations
* Research/evaluation outputs

---

## 1. Current Goal

The goal of this phase is to replace the current `TBD` AI placeholders with real AI APIs.

Current system:

```text
Frontend  ->  Backend  ->  PostgreSQL
```

Target system:

```text
Frontend  ->  Backend  ->  AI Service
               |
               v
            PostgreSQL
```

The frontend should not call the AI service directly.

The backend will call the AI service internally using Docker networking.

---

## 2. Final Local Service URLs

After implementation, local development should run:

```text
Frontend:   http://localhost:3000
Backend:    http://localhost:8000
AI Service: http://localhost:8777
Postgres:   localhost:5432
```

Internal backend-to-AI URL:

```text
http://ai:8777/api/v1
```

---

## 3. AI Service Responsibilities

The AI service is responsible for all LLM, NLP, prediction, and explainability operations.

It must provide APIs for:

* Raw requirement to Jira issue generation
* Acceptance criteria generation
* Issue type classification
* Issue priority suggestion
* Label suggestion
* Issue quality scoring
* Requirement clarity detection
* Missing field detection
* Task split recommendation
* Duplicate issue detection
* Sprint delay/risk scoring
* Business impact scoring
* Explanation generation

The backend remains responsible for:

* Authentication
* Database persistence
* Jira API calls
* Approval workflow
* Audit logging
* User/project ownership
* Routing AI results to frontend

---

## 4. AI Service Technology Stack

Use:

* Python 3.11 or 3.12
* FastAPI
* Uvicorn
* Pydantic
* Pandas
* NumPy
* scikit-learn
* sentence-transformers
* transformers, optional
* OpenAI / Gemini / Anthropic API support
* httpx
* python-dotenv
* joblib
* structlog or logging
* Docker

Recommended first LLM provider:

```text
OpenAI-compatible API
```

Keep the AI provider configurable so Gemini/Anthropic/local models can be added later.

---

## 5. AI Service Folder Structure

Create this structure:

```text
ai/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── errors.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       ├── health.py
│   │       ├── issue_generation.py
│   │       ├── issue_quality.py
│   │       ├── duplicate_check.py
│   │       ├── sprint_risk.py
│   │       ├── business_impact.py
│   │       └── explainability.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   ├── issue_generation.py
│   │   ├── issue_quality.py
│   │   ├── duplicate_check.py
│   │   ├── sprint_risk.py
│   │   ├── business_impact.py
│   │   └── explainability.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── prompt_service.py
│   │   ├── issue_generation_service.py
│   │   ├── quality_score_service.py
│   │   ├── duplicate_service.py
│   │   ├── sprint_risk_service.py
│   │   ├── business_impact_service.py
│   │   └── explanation_service.py
│   │
│   ├── prompts/
│   │   ├── issue_generation_prompt.py
│   │   ├── quality_score_prompt.py
│   │   ├── sprint_risk_prompt.py
│   │   ├── business_impact_prompt.py
│   │   └── explanation_prompt.py
│   │
│   ├── models/
│   │   ├── delay_model.py
│   │   ├── sprint_risk_model.py
│   │   ├── duplicate_model.py
│   │   └── model_registry.py
│   │
│   ├── utils/
│   │   ├── text_cleaner.py
│   │   ├── score_utils.py
│   │   ├── json_parser.py
│   │   └── validation.py
│   │
│   └── research/
│       ├── metrics.py
│       ├── experiment_logger.py
│       └── evaluator.py
│
├── scripts/
│   ├── check_env.py
│   ├── test_llm_prompts.py
│   ├── run_quality_eval.py
│   ├── train_delay_model.py
│   ├── evaluate_predictions.py
│   ├── build_embeddings.py
│   └── export_metrics.py
│
├── datasets/
│   ├── README.md
│   ├── sample_issues.csv
│   └── sample_sprints.csv
│
├── notebooks/
│   └── research_experiments.ipynb
│
├── tests/
│   ├── test_health.py
│   ├── test_issue_generation.py
│   ├── test_quality_score.py
│   └── test_sprint_risk.py
│
├── requirements.txt
├── pyproject.toml
├── .env.dev.example
├── .env.prod.example
└── README.md
```

---

## 6. API Prefix Rule

All AI service routes must use:

```text
/api/v1
```

Example:

```text
/api/v1/issue/generate
/api/v1/issue/quality-score
/api/v1/sprint/risk-score
```

---

## 7. AI Service Routes

### Health

```text
GET /api/v1/health
```

Response:

```json
{
  "success": true,
  "message": "SprintMind AI service is running",
  "data": {
    "status": "ok",
    "service": "ai",
    "version": "1.0.0"
  }
}
```

---

## 8. Issue Generation API

### Route

```text
POST /api/v1/issue/generate
```

### Purpose

Convert raw requirement/task text into a structured Jira issue draft.

### Request

```json
{
  "rawTitle": "Need login",
  "rawDescription": "User should login with email and password. Need validation and error message.",
  "businessGoal": "Allow users to access the dashboard securely",
  "projectContext": "SprintMind AI dashboard auth module",
  "preferredIssueType": "Story",
  "preferredPriority": "Medium"
}
```

### Response

```json
{
  "success": true,
  "message": "Issue generated successfully",
  "data": {
    "title": "Implement email and password login flow",
    "description": "Build a secure login flow that allows users to authenticate using email and password.",
    "issueType": "Story",
    "priority": "Medium",
    "labels": ["auth", "frontend", "backend"],
    "acceptanceCriteria": [
      "User can enter email and password",
      "System validates required fields",
      "Invalid credentials show an error message",
      "Successful login redirects user to dashboard"
    ],
    "suggestedSubtasks": [
      "Create login UI",
      "Implement backend login API integration",
      "Add validation and error handling",
      "Test successful and failed login"
    ],
    "confidence": 0.86
  }
}
```

---

## 9. Issue Quality Score API

### Route

```text
POST /api/v1/issue/quality-score
```

### Purpose

Score a Jira issue based on clarity, completeness, testability, dependencies, and business value.

### Request

```json
{
  "title": "Fix dashboard",
  "description": "Dashboard has problems and needs fixing.",
  "acceptanceCriteria": [],
  "issueType": "Task",
  "priority": "Medium",
  "labels": ["dashboard"]
}
```

### Response

```json
{
  "success": true,
  "message": "Issue quality score generated",
  "data": {
    "overallScore": 42,
    "clarityScore": 35,
    "completenessScore": 40,
    "testabilityScore": 30,
    "dependencyClarityScore": 50,
    "businessValueScore": 55,
    "problems": [
      "Description is too broad",
      "Acceptance criteria are missing",
      "Expected behavior is not clearly defined",
      "No testable outcome is mentioned"
    ],
    "recommendations": [
      "Add clear acceptance criteria",
      "Mention the exact dashboard problem",
      "Define expected result",
      "Add screenshots or reproduction steps if it is a bug"
    ],
    "confidence": 0.82
  }
}
```

---

## 10. Duplicate Issue Detection API

### Route

```text
POST /api/v1/issue/duplicate-check
```

### Purpose

Detect whether a new issue is similar to existing issues.

### Request

```json
{
  "candidateIssue": {
    "title": "Add CSV export to dashboard",
    "description": "Users should export dashboard report as CSV"
  },
  "existingIssues": [
    {
      "id": "1",
      "title": "Export dashboard reports",
      "description": "Allow users to export sprint health reports as CSV and PDF"
    },
    {
      "id": "2",
      "title": "Fix login validation",
      "description": "Show proper error for invalid login"
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "message": "Duplicate check completed",
  "data": {
    "isPotentialDuplicate": true,
    "matches": [
      {
        "id": "1",
        "similarityScore": 0.84,
        "reason": "Both issues request CSV export for dashboard/report data."
      }
    ]
  }
}
```

---

## 11. Sprint Risk Score API

### Route

```text
POST /api/v1/sprint/risk-score
```

### Purpose

Estimate sprint delivery risk using issue data, team capacity, blocked tasks, priority, and workload.

### Request

```json
{
  "sprintName": "Sprint 12",
  "teamCapacity": 80,
  "committedPoints": 95,
  "issues": [
    {
      "id": "ISSUE-1",
      "title": "Build Jira connection flow",
      "priority": "High",
      "status": "In Progress",
      "storyPoints": 13,
      "assignee": "Developer A",
      "blocked": false,
      "qualityScore": 70
    },
    {
      "id": "ISSUE-2",
      "title": "Implement AI risk score",
      "priority": "High",
      "status": "To Do",
      "storyPoints": 21,
      "assignee": "Developer B",
      "blocked": true,
      "qualityScore": 48
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "message": "Sprint risk score generated",
  "data": {
    "riskLevel": "High",
    "riskScore": 82,
    "capacityRisk": 88,
    "blockerRisk": 75,
    "qualityRisk": 70,
    "deliveryConfidence": 42,
    "mainRiskFactors": [
      "Committed story points exceed team capacity",
      "High-priority task is blocked",
      "Large task has low quality score"
    ],
    "recommendations": [
      "Move lower-priority tasks to next sprint",
      "Unblock ISSUE-2 before sprint midpoint",
      "Split large AI task into smaller subtasks"
    ],
    "confidence": 0.8
  }
}
```

---

## 12. Business Impact Score API

### Route

```text
POST /api/v1/business/impact-score
```

### Purpose

Estimate business impact of an issue or sprint risk.

### Request

```json
{
  "title": "Payment validation API",
  "description": "Implement payment validation before checkout confirmation",
  "priority": "High",
  "customerFacing": true,
  "releaseCritical": true,
  "blocked": false,
  "delayRisk": "High"
}
```

### Response

```json
{
  "success": true,
  "message": "Business impact score generated",
  "data": {
    "impactLevel": "High",
    "impactScore": 88,
    "costOfDelay": "High",
    "customerImpact": "High",
    "releaseRisk": "High",
    "reasoning": [
      "The issue is customer-facing",
      "The issue is release-critical",
      "Delay risk is already high"
    ],
    "recommendedAction": [
      "Assign senior engineer",
      "Add QA test coverage early",
      "Track this issue daily until completion"
    ],
    "confidence": 0.84
  }
}
```

---

## 13. Explainability API

### Route

```text
POST /api/v1/explain

```

### Purpose

Generate a simple explanation for any AI-generated score or recommendation.

### Request

```json
{
  "scoreType": "SPRINT_RISK",
  "score": 82,
  "riskLevel": "High",
  "factors": [
    "Committed story points exceed team capacity",
    "High-priority issue is blocked",
    "Large task has low quality score"
  ]
}
```

### Response

```json
{
  "success": true,
  "message": "Explanation generated",
  "data": {
    "summary": "This sprint has high delivery risk because the committed work is larger than the available team capacity and one high-priority task is blocked.",
    "detailedExplanation": [
      "The sprint has 95 committed story points while the team capacity is 80.",
      "A high-priority issue is currently blocked.",
      "One large task has a low issue quality score, which increases clarification and rework risk."
    ],
    "recommendedNextSteps": [
      "Reduce sprint scope",
      "Resolve blocker immediately",
      "Improve the low-quality issue before development starts"
    ]
  }
}
```

---

## 14. AI Pipeline Design

### Issue Generation Pipeline

```text
Raw task input
    ↓
Text cleaning
    ↓
Prompt building
    ↓
LLM call
    ↓
JSON validation
    ↓
Fallback repair if invalid JSON
    ↓
Structured issue response
```

### Quality Scoring Pipeline

```text
Issue fields
    ↓
Rule-based checks
    ↓
LLM review
    ↓
Score normalization
    ↓
Problem list
    ↓
Recommendation list
```

### Sprint Risk Pipeline

```text
Sprint data
    ↓
Feature extraction
    ↓
Rule-based baseline score
    ↓
Optional ML model score
    ↓
LLM explanation
    ↓
Risk recommendation
```

### Business Impact Pipeline

```text
Issue/sprint metadata
    ↓
Business rule scoring
    ↓
Impact classification
    ↓
LLM explanation
    ↓
Recommended action
```

---

## 15. LLM Service Design

Create a reusable `llm_service.py`.

Responsibilities:

* Select provider
* Build request payload
* Call LLM API
* Handle timeout
* Handle retries
* Parse JSON response
* Handle invalid JSON
* Return normalized response

Supported providers:

```text
openai
gemini
anthropic
mock
```

For local development, support a `mock` provider so the app works without paid API calls.

Example env:

```env
MODEL_PROVIDER=mock
```

When `MODEL_PROVIDER=mock`, return fixed sample AI responses.

---

## 16. Prompt Requirements

Prompts must be stored separately inside:

```text
ai/app/prompts/
```

Each prompt should clearly request valid JSON only.

Prompt rules:

* Do not return markdown
* Do not return explanations outside JSON
* Always include confidence score
* Always include recommendations
* Always use safe and neutral language
* Never expose secrets or private data

---

## 17. Example Issue Generation Prompt Requirements

The issue generation prompt must instruct the LLM to return:

```text
title
description
issueType
priority
labels
acceptanceCriteria
suggestedSubtasks
confidence
```

The prompt must say:

```text
Return only valid JSON. Do not include markdown. Do not include extra text.
```

---

## 18. Scoring Rules

Use score range:

```text
0 to 100
```

Score interpretation:

```text
0-39   = Poor / High risk
40-59  = Needs improvement / Medium-high risk
60-79  = Good / Medium-low risk
80-100 = Strong / Low risk
```

Risk labels:

```text
Low
Medium
High
Critical
```

---

## 19. Issue Quality Scoring Logic

Use a hybrid approach:

### Rule-based score

Check:

* Title length
* Description length
* Acceptance criteria exists
* Issue type exists
* Priority exists
* Labels exist
* Dependencies mentioned
* Testable outcome present

### LLM-based score

Ask LLM to judge:

* Clarity
* Completeness
* Testability
* Business value
* Scope
* Ambiguity
* Suggested improvements

### Final score

Combine:

```text
Final Quality Score = 60% rule-based + 40% LLM-based
```

For MVP, rule-based scoring can be enough.

---

## 20. Sprint Risk Scoring Logic

Use a hybrid approach.

Risk factors:

* Committed points > team capacity
* Blocked high-priority issues
* Too many large issues
* Too many low-quality issues
* Too many unassigned issues
* Too many tasks in To Do near sprint midpoint
* Reopened issues
* Dependency-heavy tasks
* High business impact issues at risk

MVP formula:

```text
Sprint Risk Score =
capacity risk
+ blocker risk
+ quality risk
+ workload risk
+ priority risk
```

Normalize final score to 0-100.

---

## 21. Business Impact Logic

Business impact should consider:

* Customer-facing status
* Release-critical status
* Priority
* Delay risk
* Blocked status
* Revenue/compliance impact
* Dependency count
* Number of affected users, if available

MVP impact labels:

```text
Low
Medium
High
Critical
```

---

## 22. Docker Integration

The AI service must run as a Docker container.

Add:

```text
docker/Dockerfile.ai
```

Update:

```text
docker-compose.dev.yml
```

Add service:

```yaml
ai:
  build:
    context: .
    dockerfile: docker/Dockerfile.ai
  ports:
    - "8777:8777"
  env_file:
    - ai/.env.dev
  volumes:
    - ./ai:/app
```

Backend environment must include:

```env
AI_SERVICE_URL=http://ai:8777/api/v1
```

Backend depends on AI:

```yaml
backend:
  depends_on:
    - postgres
    - ai
```

---

## 23. Dockerfile.ai Requirement

File:

```text
docker/Dockerfile.ai
```

Requirements:

* Use Python 3.11 or 3.12
* Set working directory to `/app`
* Copy AI requirements
* Install dependencies
* Copy AI source
* Expose port `8777`
* Run Uvicorn

Expected command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8777 --reload
```

---

## 24. AI Environment Files

Create:

```text
ai/.env.dev.example
ai/.env.prod.example
```

### ai/.env.dev.example

```env
APP_ENV=development
APP_NAME=SprintMind AI Service
APP_HOST=0.0.0.0
APP_PORT=8777

MODEL_PROVIDER=mock
LLM_MODEL_NAME=mock-model
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=

REQUEST_TIMEOUT_SECONDS=30
MAX_RETRIES=2

BACKEND_INTERNAL_API_URL=http://backend:8000/api/v1

LOG_LEVEL=debug
```

### ai/.env.prod.example

```env
APP_ENV=production
APP_NAME=SprintMind AI Service
APP_HOST=0.0.0.0
APP_PORT=8777

MODEL_PROVIDER=openai
LLM_MODEL_NAME=gpt-4o-mini
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=

REQUEST_TIMEOUT_SECONDS=30
MAX_RETRIES=2

BACKEND_INTERNAL_API_URL=http://backend:8000/api/v1

LOG_LEVEL=info
```

---

## 25. run.sh Update

Update `scripts/run.sh --dev` so it also handles the AI service.

Expected behavior:

1. Create `frontend/.env.dev` if missing
2. Create `backend/.env.dev` if missing
3. Create `ai/.env.dev` if missing
4. Build frontend image
5. Build backend image
6. Build AI image
7. Start PostgreSQL
8. Start AI service
9. Start backend
10. Run Prisma migrations
11. Start frontend
12. Print all service URLs

Expected output:

```text
SprintMind AI is running

Frontend:   http://localhost:3000
Backend:    http://localhost:8000
AI Service: http://localhost:8777
Postgres:   localhost:5432
```

---

## 26. Backend Integration

The backend should replace `TBD` placeholder logic with real AI service calls.

Backend AI client file:

```text
backend/app/services/ai_client.py
```

Responsibilities:

* Read `AI_SERVICE_URL`
* Send POST requests to AI service
* Handle timeout
* Handle AI service error
* Return safe fallback if AI service is unavailable

Backend should call:

```text
POST http://ai:8777/api/v1/issue/generate
POST http://ai:8777/api/v1/issue/quality-score
POST http://ai:8777/api/v1/issue/duplicate-check
POST http://ai:8777/api/v1/sprint/risk-score
POST http://ai:8777/api/v1/business/impact-score
POST http://ai:8777/api/v1/explain
```

---

## 27. Backend Fallback Rule

If AI service is unavailable, backend must not crash.

Return:

```json
{
  "success": false,
  "message": "AI service unavailable",
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE"
  }
}
```

Frontend should show a clear error.

---

## 28. Frontend Integration

Frontend should continue to call backend only.

Frontend must not call:

```text
http://localhost:8777
```

Frontend should call:

```text
http://localhost:8000/api/v1/...
```

Backend will forward the request to AI internally.

Example frontend flow:

```text
User imports issue
    ↓
Frontend calls backend /api/v1/issues/import
    ↓
User clicks Analyze
    ↓
Frontend calls backend /api/v1/issues/{id}/analyze
    ↓
Backend calls AI service
    ↓
Backend saves AI result
    ↓
Frontend shows generated issue, quality score, risk, recommendation
```

---

## 29. Backend Routes to Add or Update

Add/update these backend routes:

```text
POST /api/v1/issues/{issue_id}/analyze
POST /api/v1/issues/{issue_id}/quality-score
POST /api/v1/issues/{issue_id}/business-impact
POST /api/v1/sprints/{sprint_id}/risk-score
POST /api/v1/issues/{issue_id}/generate-recommendations
```

These routes call the AI service internally.

---

## 30. Data Persistence

AI results should be saved in PostgreSQL through backend models.

Recommended tables:

```text
IssueAnalysis
IssueQualityScore
RiskPrediction
BusinessImpactScore
AIRecommendation
AIRequestLog
```

---

## 31. Suggested New Prisma Models

### IssueAnalysis

Fields:

```text
id
issueDraftId
generatedTitle
generatedDescription
issueType
priority
labels
acceptanceCriteria
suggestedSubtasks
confidence
createdAt
updatedAt
```

### IssueQualityScore

Fields:

```text
id
issueDraftId
overallScore
clarityScore
completenessScore
testabilityScore
dependencyClarityScore
businessValueScore
problems
recommendations
confidence
createdAt
updatedAt
```

### RiskPrediction

Fields:

```text
id
issueDraftId
sprintId
riskType
riskLevel
riskScore
mainRiskFactors
recommendations
confidence
createdAt
updatedAt
```

### BusinessImpactScore

Fields:

```text
id
issueDraftId
impactLevel
impactScore
costOfDelay
customerImpact
releaseRisk
reasoning
recommendedAction
confidence
createdAt
updatedAt
```

### AIRecommendation

Fields:

```text
id
issueDraftId
recommendationType
title
description
reason
status
confidence
createdAt
updatedAt
```

### AIRequestLog

Fields:

```text
id
userId
route
provider
model
status
latencyMs
errorMessage
createdAt
```

---

## 32. Mock Mode Requirement

For development, the AI service must support mock mode.

When:

```env
MODEL_PROVIDER=mock
```

The AI service should return deterministic fake responses.

This helps:

* Avoid paid API usage during development
* Keep Docker startup simple
* Allow frontend/backend testing without external AI keys
* Make demos reliable

Mock mode should support all AI routes.

---

## 33. Real LLM Mode

When using real LLM provider:

```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=your_key
LLM_MODEL_NAME=gpt-4o-mini
```

The service should:

* Call the model
* Request JSON-only output
* Validate output with Pydantic
* Retry if output is invalid
* Return normalized response

---

## 34. JSON Validation Requirement

All LLM outputs must be validated.

Rules:

* Never trust raw LLM text
* Parse as JSON
* Validate with Pydantic schema
* Repair once if invalid
* Return error if still invalid
* Never return broken JSON to backend

---

## 35. Error Response Format

All AI errors should follow:

```json
{
  "success": false,
  "message": "Error message",
  "error": {
    "code": "ERROR_CODE",
    "details": "Optional details"
  }
}
```

Common error codes:

```text
AI_INVALID_INPUT
AI_PROVIDER_ERROR
AI_TIMEOUT
AI_INVALID_JSON
AI_MODEL_NOT_CONFIGURED
AI_INTERNAL_ERROR
```

---

## 36. Security Requirements

The AI service must:

* Never expose API keys
* Never log secrets
* Never log Jira tokens
* Never log full private issue data in production
* Use environment variables only
* Support safe debug logs in development
* Return safe errors to backend
* Validate input size
* Reject extremely large payloads

---

## 37. Privacy Requirements

The AI service must handle data carefully.

Before sending text to external LLM APIs, the backend or AI service should support optional redaction.

Redact:

* Emails
* Phone numbers
* Access tokens
* URLs
* Client names
* Internal project names
* Personal names if required

For research/demo use, prefer:

* Public Jira datasets
* Synthetic issues
* Anonymized data
* Demo Jira workspace

---

## 38. Research Mode

The AI service should support research logging.

Research logs should include:

* Input type
* Model provider
* Model name
* Prompt version
* Output score
* Confidence
* Latency
* Evaluation metric
* Timestamp

Do not log sensitive text in production.

---

## 39. Evaluation Scripts

Create scripts:

```text
ai/scripts/run_quality_eval.py
ai/scripts/train_delay_model.py
ai/scripts/evaluate_predictions.py
ai/scripts/test_llm_prompts.py
ai/scripts/export_metrics.py
```

### run_quality_eval.py

Purpose:

* Run issue quality scoring on sample issues
* Compare raw vs improved issues
* Export metrics

### train_delay_model.py

Purpose:

* Train baseline delay prediction model
* Use sample/public issue data
* Save model artifact

### evaluate_predictions.py

Purpose:

* Calculate F1, AUC, precision, recall, MAE

### test_llm_prompts.py

Purpose:

* Test prompt outputs
* Validate JSON structure
* Compare prompt versions

### export_metrics.py

Purpose:

* Export research metrics as CSV/JSON

---

## 40. Dataset Folder

Use:

```text
ai/datasets/
```

Initial files:

```text
sample_issues.csv
sample_sprints.csv
README.md
```

Sample issue columns:

```text
id
title
description
issue_type
priority
status
assignee
story_points
blocked
comments_count
status_changes
quality_score
cycle_time_days
was_delayed
```

Sample sprint columns:

```text
id
sprint_name
team_capacity
committed_points
completed_points
blocked_issues
high_priority_issues
reopened_issues
was_delayed
```

---

## 41. Testing Requirements

Use pytest.

Required tests:

```text
tests/test_health.py
tests/test_issue_generation.py
tests/test_quality_score.py
tests/test_duplicate_check.py
tests/test_sprint_risk.py
tests/test_business_impact.py
```

Each test should verify:

* API returns success
* Response schema is valid
* Scores are inside 0-100
* Risk labels are valid
* Mock mode works
* Invalid input returns proper error

---

## 42. AI Health Check

The AI health endpoint should also return provider info.

```json
{
  "success": true,
  "message": "SprintMind AI service is running",
  "data": {
    "status": "ok",
    "service": "ai",
    "provider": "mock",
    "model": "mock-model"
  }
}
```

---

## 43. Development Flow

### Step 1: Create AI service folder

```bash
mkdir -p ai
```

### Step 2: Add AI files and structure

Create the folder structure from this guide.

### Step 3: Add environment file

```bash
cp ai/.env.dev.example ai/.env.dev
```

### Step 4: Keep mock mode first

```env
MODEL_PROVIDER=mock
```

### Step 5: Update Docker Compose

Add AI service to `docker-compose.dev.yml`.

### Step 6: Update backend env

Add:

```env
AI_SERVICE_URL=http://ai:8777/api/v1
```

### Step 7: Run full stack

```bash
./scripts/run.sh --dev
```

### Step 8: Test AI health

```bash
curl http://localhost:8777/api/v1/health
```

### Step 9: Test backend-to-AI flow

Use frontend issue analysis flow or call backend route directly.

---

## 44. Production Flow

In production:

```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=
LLM_MODEL_NAME=gpt-4o-mini
```

Production should run:

```text
Frontend  -> Cloudflare Pages
Backend   -> Cloudflare Container
AI        -> Cloudflare Container
Database  -> AWS RDS PostgreSQL
```

The AI service should not be publicly exposed unless needed.

---

## 45. Implementation Priority

### Phase 1 - AI Service Foundation

Implement:

* FastAPI app
* Health route
* Config
* Logging
* Mock provider
* Dockerfile.ai
* docker-compose AI service
* Backend AI client

### Phase 2 - Issue Intelligence

Implement:

* Issue generation
* Acceptance criteria generation
* Issue quality scoring
* Backend route integration
* Frontend display integration

### Phase 3 - Risk Intelligence

Implement:

* Sprint risk score
* Issue delay risk
* Business impact score
* Explanation generator

### Phase 4 - Research Features

Implement:

* Evaluation scripts
* Dataset support
* Experiment logging
* Metrics export
* Research report data

---

## 46. Minimum Working AI MVP

The AI MVP is complete when:

```text
./scripts/run.sh --dev
```

starts:

```text
Frontend:   http://localhost:3000
Backend:    http://localhost:8000
AI Service: http://localhost:8777
Postgres:   localhost:5432
```

And the user can:

1. Login
2. Connect Jira
3. Create/import issue draft
4. Click AI analyze
5. Backend calls AI service
6. AI returns generated issue content
7. Backend saves AI result
8. Frontend displays:

   * generated title
   * generated description
   * acceptance criteria
   * quality score
   * recommendations
   * risk/business impact score
9. User sends result to approval
10. User approves/rejects suggestion

---

## 47. Final Success Criteria

This AI phase is successful when:

* AI service runs as its own container
* Backend communicates with AI using internal Docker URL
* Frontend does not directly call AI
* Mock mode works without API keys
* Real provider mode can be enabled by env variables
* Issue generation works
* Quality scoring works
* Sprint risk scoring works
* Business impact scoring works
* AI results are saved in PostgreSQL
* AI routes return consistent JSON
* Docker `run.sh --dev` starts the full system
* AI outputs are research-ready and explainable

---

## 48. Final Research Pitch

SprintMind AI uses LLMs and software analytics to improve agile project management. It converts unstructured requirements into high-quality Jira issues, scores requirement quality, predicts sprint delivery risks, estimates business impact, and provides explainable recommendations for human-approved workflow automation.

The AI service is the research core of the project. It enables experimentation with prompt design, issue quality evaluation, sprint risk prediction, explainable AI, and business value measurement for agile software teams.
