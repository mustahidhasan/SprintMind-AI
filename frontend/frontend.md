Below is the **complete frontend flow idea** for **SprintMind AI**.

Frontend goal:

> A clean Next.js dashboard where users can sign in, connect Jira using API token, import/enter tasks, run AI analysis, review suggestions, approve Jira updates, and monitor sprint/project risk.

This matches the project’s core modules: requirement-to-ticket pipeline, LLM issue builder, quality intelligence, sprint risk prediction, business impact engine, human approval, and dashboard. 

---

# Frontend App Structure

Use **Next.js App Router + TypeScript + Axios**.

```text
frontend/src/
│
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   │
│   ├── auth/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   └── reset-password/page.tsx
│   │
│   ├── dashboard/page.tsx
│   │
│   ├── onboarding/
│   │   ├── page.tsx
│   │   ├── connect-jira/page.tsx
│   │   └── select-project/page.tsx
│   │
│   ├── jira/
│   │   ├── connection/page.tsx
│   │   ├── projects/page.tsx
│   │   ├── boards/page.tsx
│   │   └── sync/page.tsx
│   │
│   ├── issues/
│   │   ├── page.tsx
│   │   ├── import/page.tsx
│   │   ├── analyze/page.tsx
│   │   ├── drafts/page.tsx
│   │   └── [issueId]/page.tsx
│   │
│   ├── sprints/
│   │   ├── page.tsx
│   │   └── [sprintId]/page.tsx
│   │
│   ├── approvals/page.tsx
│   ├── recommendations/page.tsx
│   ├── reports/page.tsx
│   └── settings/page.tsx
│
├── components/
├── features/
├── lib/
├── hooks/
├── types/
└── middleware.ts
```

---

# Main User Flow

```text
User registers/logs in
        ↓
User connects Jira with base URL + email + API token
        ↓
System validates Jira connection
        ↓
User selects Jira project and board
        ↓
System syncs projects, boards, sprints, and issue types
        ↓
User imports tasks from CSV / Google Sheet / manual input
        ↓
AI converts raw tasks into Jira issue drafts
        ↓
AI scores issue quality and detects missing information
        ↓
AI predicts sprint risk and business impact
        ↓
User reviews AI suggestions
        ↓
User approves selected issues/updates
        ↓
Backend creates/updates Jira issues
        ↓
Dashboard shows sprint health, risks, workload, and reports
```

---

# 1. Auth Flow

## Pages

```text
/auth/login
/auth/register
/auth/forgot-password
/auth/reset-password
```

## Features

Basic auth should include:

* Register
* Login
* Logout
* Forgot password
* Reset password
* Auth token storage
* Protected routes
* User profile
* Organization/workspace support

## Frontend state

Store:

```text
accessToken
refreshToken
user
organization
selectedProject
selectedJiraConnection
```

## Auth API routes

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
POST /api/v1/auth/forgot-password
POST /api/v1/auth/reset-password
GET  /api/v1/auth/me
```

## Frontend behavior

After login:

```text
If user has no Jira connection → redirect to /onboarding/connect-jira
If user has Jira connection → redirect to /dashboard
```

---

# 2. Onboarding Flow

## Goal

Help the user connect Jira and select a working board.

## Pages

```text
/onboarding
/onboarding/connect-jira
/onboarding/select-project
```

## Step 1: Welcome

Show:

```text
Welcome to SprintMind AI
Connect your Jira workspace to start analyzing tickets, sprint risks, and workflow quality.
```

Actions:

```text
Connect Jira
Skip for demo mode
```

## Step 2: Connect Jira

Form fields:

```text
Jira Base URL
Jira Email
Jira API Token
Connection Name
```

Example:

```text
Jira Base URL: https://yourcompany.atlassian.net
Email: user@company.com
API Token: ********
Connection Name: Company Jira
```

Button:

```text
Test Connection
```

After successful test:

```text
Save Connection
```

## Step 3: Select project and board

After connection, fetch:

* Jira projects
* Boards
* Active sprints
* Issue types
* Priorities
* Labels/components if available

User selects:

```text
Project
Board
Default issue type
Default sprint
```

Then:

```text
Finish Setup → Dashboard
```

---

# 3. Jira Connection Flow

## Page

```text
/jira/connection
```

## Purpose

Manage Jira API connection.

## Sections

### Connection Status Card

Show:

```text
Status: Connected / Failed / Not connected
Jira URL
Connected email
Last sync time
Selected project
Selected board
```

### Actions

```text
Test Connection
Reconnect
Remove Connection
Sync Jira Metadata
```

### Security Notice

Show:

```text
Your Jira token is encrypted and stored securely. SprintMind AI never exposes your token in logs or frontend responses.
```

## API routes

```text
POST /api/v1/jira/connect
POST /api/v1/jira/test-connection
GET  /api/v1/jira/connection
DELETE /api/v1/jira/connection
POST /api/v1/jira/sync
GET  /api/v1/jira/projects
GET  /api/v1/jira/boards
GET  /api/v1/jira/sprints
```

---

# 4. Dashboard Flow

## Page

```text
/dashboard
```

## Purpose

Show the project health overview.

## Dashboard cards

### Top Summary Cards

```text
Total Issues Synced
High Risk Issues
Sprint Risk Score
Average Issue Quality
Pending Approvals
Estimated Cost of Delay
```

### Main Sections

```text
Sprint Health
Issue Quality Trend
High Risk Issues
Blocked / Delayed Tasks
Team Workload
AI Recommendations
Business Impact Summary
```

## Example dashboard layout

```text
-------------------------------------------------
SprintMind AI Dashboard
-------------------------------------------------

[Current Sprint Risk: High] [Avg Quality: 72/100]
[Pending Approvals: 12]    [Cost of Delay: High]

Sprint Health
- Sprint overload: 86%
- Blocked issues: 5
- Delay risk: High

High Risk Issues
- API payment validation
- Dashboard export bug
- Role permission update

AI Recommendations
- Split large backend issue
- Add acceptance criteria to 8 tickets
- Move 3 low-priority tasks to next sprint
```

---

# 5. Issue Import Flow

## Page

```text
/issues/import
```

## Purpose

Import raw tasks from multiple sources.

## Import methods

```text
Manual input
CSV upload
Google Sheet link
Existing Jira sync
Meeting notes paste
Requirement document paste
```

## Manual input form

Fields:

```text
Raw task title
Raw description
Business goal
Priority
Expected deadline
Optional notes
```

## CSV upload columns

Recommended CSV format:

```text
title
description
priority
component
assignee
deadline
business_value
notes
```

## After import

User clicks:

```text
Analyze with AI
```

Then redirect:

```text
/issues/analyze
```

---

# 6. AI Issue Analysis Flow

## Page

```text
/issues/analyze
```

## Purpose

AI converts raw tasks into structured Jira issue drafts.

## For each imported task, show:

### Raw Input

```text
Original task text
```

### AI Generated Output

```text
Generated title
Generated description
Acceptance criteria
Issue type
Priority
Labels
Suggested assignee
Suggested sprint
Dependencies
```

### Quality Score

```text
Clarity: 75/100
Completeness: 68/100
Testability: 80/100
Dependency clarity: 60/100
Overall quality: 71/100
```

### Risk Score

```text
Delay risk: Medium
Reopen risk: Low
Business impact: High
```

### Recommended Actions

```text
Add missing acceptance criteria
Split this into 2 subtasks
Confirm API dependency
Move to next sprint if capacity is overloaded
```

## User actions

```text
Edit AI Draft
Regenerate
Accept Suggestion
Reject Suggestion
Send to Approval
Create Jira Issue
```

---

# 7. Issue Drafts Flow

## Page

```text
/issues/drafts
```

## Purpose

Show AI-generated drafts before creating Jira issues.

## Table columns

```text
Title
Issue Type
Priority
Quality Score
Delay Risk
Business Impact
Status
Actions
```

## Draft statuses

```text
Generated
Edited
Needs Review
Approved
Rejected
Created in Jira
```

## Actions

```text
View
Edit
Approve
Reject
Create in Jira
Bulk Approve
Bulk Create
```

---

# 8. Human Approval Flow

## Page

```text
/approvals
```

## Purpose

PM/team lead reviews AI actions before Jira update.

## Approval types

```text
Create new Jira issue
Update existing issue
Change priority
Add labels
Assign sprint
Link dependency
Split task
Add acceptance criteria
```

## Approval card example

```text
AI Suggestion:
Create Story: "Implement payment validation API"

Reason:
The raw requirement describes backend validation logic and user-facing checkout failure handling.

Quality Score:
82/100

Risk:
Medium delay risk due to payment dependency.

Actions:
[Approve] [Edit Before Approve] [Reject]
```

## After approval

Backend sends request to Jira API.

Then UI shows:

```text
Jira issue created successfully: PROJ-123
```

---

# 9. Jira Issues Flow

## Page

```text
/issues
```

## Purpose

Show synced and AI-created Jira issues.

## Filters

```text
Project
Sprint
Issue type
Priority
Assignee
Risk level
Quality score
Status
Business impact
```

## Table columns

```text
Jira Key
Title
Status
Assignee
Priority
Quality Score
Delay Risk
Business Impact
Last Updated
```

## Issue detail page

```text
/issues/[issueId]
```

Sections:

```text
Original Jira data
AI analysis
Quality score breakdown
Risk explanation
Business impact
Recommended actions
Approval history
Automation logs
```

---

# 10. Sprint Intelligence Flow

## Page

```text
/sprints
/sprints/[sprintId]
```

## Purpose

Show sprint-level risk and workload.

## Sprint detail sections

### Sprint Summary

```text
Sprint name
Start date
End date
Total issues
Completed issues
Blocked issues
High risk issues
Sprint risk score
```

### Sprint Risk Breakdown

```text
Capacity risk
Delay risk
Dependency risk
Reopen risk
Business impact risk
```

### Team Workload

```text
Assignee
Assigned issues
High risk issues
Estimated load
Overload status
```

### AI Recommendations

```text
Move low-priority tasks to next sprint
Split large issues
Add acceptance criteria
Assign reviewer for high-risk issue
Reduce sprint scope by 15%
```

---

# 11. Recommendations Flow

## Page

```text
/recommendations
```

## Purpose

Central place for all AI suggestions.

## Recommendation types

```text
Improve issue quality
Split large task
Add acceptance criteria
Change priority
Move sprint
Assign reviewer
Link dependency
Flag blocker
Reduce sprint scope
```

## Recommendation statuses

```text
New
Viewed
Accepted
Rejected
Applied
```

## Card example

```text
Recommendation:
Split "Build reporting module" into 3 smaller tasks.

Reason:
The issue has broad scope, missing test cases, and high delay risk.

Business value:
Reducing scope may lower sprint risk by 18%.

Actions:
[Accept] [Reject] [Create Drafts]
```

---

# 12. Reports Flow

## Page

```text
/reports
```

## Purpose

Generate research/business reports.

## Report types

```text
Sprint Health Report
Issue Quality Report
Business Impact Report
Delay Risk Report
AI Recommendation Report
Research Experiment Report
```

## Export options

```text
PDF
CSV
JSON
```

## Report sections

```text
Summary
Key metrics
High-risk issues
Root causes
Recommendations
Business impact
Model confidence
```

---

# 13. Settings Flow

## Page

```text
/settings
```

## Sections

```text
Profile
Organization
Jira connection
AI settings
Model settings
Security
Billing/future SaaS settings
Data privacy
```

## AI settings

```text
Model provider
Model name
Temperature
Max tokens
Enable/disable business impact scoring
Enable/disable auto quality score
Enable/disable risk prediction
```

---

# 14. Frontend Components

## Common components

```text
Button
Input
Textarea
Select
Modal
Tabs
Badge
Card
Table
LoadingSpinner
EmptyState
ErrorState
ConfirmDialog
ToastNotification
```

## Feature components

```text
JiraConnectionForm
ProjectSelector
BoardSelector
IssueImportForm
CSVUploader
ManualTaskInput
IssueAnalysisCard
QualityScoreCard
RiskScoreBadge
BusinessImpactCard
ApprovalActionCard
SprintHealthCard
RecommendationCard
WorkloadChart
ReportExportButton
```

---

# 15. Frontend State Management

Use simple state first.

Recommended:

```text
React Query / TanStack Query for API data
Zustand for app-level state
React Hook Form for forms
Zod for validation
Axios for API calls
```

State groups:

```text
authStore
jiraStore
projectStore
issueStore
approvalStore
settingsStore
```

---

# 16. Suggested Frontend Pages by Priority

## Phase 1: Basic app

Build first:

```text
Login
Register
Dashboard
Connect Jira
Select Project
Settings
```

## Phase 2: Core operation

Build next:

```text
Issue Import
Issue Analyze
Issue Drafts
Approval Page
Jira Issues List
Issue Detail
```

## Phase 3: Intelligence

Build later:

```text
Sprint Dashboard
Recommendations
Reports
Business Impact Dashboard
Research Metrics
```

---

# 17. Full Frontend Flow Summary

```text
1. User signs up/logs in
2. User connects Jira using base URL, email, and API token
3. Frontend tests Jira connection through backend
4. User selects Jira project and board
5. System syncs Jira metadata
6. User imports raw tasks from CSV/manual/Google Sheet
7. User sends tasks for AI analysis
8. AI generates structured Jira issue drafts
9. Frontend shows quality score, risk score, and recommendations
10. User edits or approves AI-generated drafts
11. Backend creates approved issues in Jira
12. Dashboard updates sprint health, issue risk, workload, and business impact
13. User exports reports for research/professor/demo purpose
```

This frontend flow is enough to build a strong MVP and also present the project as a serious research/product system.
