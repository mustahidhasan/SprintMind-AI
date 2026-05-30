from fastapi import APIRouter, Depends, HTTPException
from time import perf_counter
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.core.config import settings
from app.models.entities import (
    AIRecommendation,
    ApprovalRequest,
    BusinessImpactScore,
    DraftStatus,
    IssueAnalysis,
    IssueDraft,
    IssueQualityScore,
    User,
)
from app.schemas.issue import IssueImportRequest
from app.services.ai_client import AIClient
from app.services.ai_request_log_service import log_ai_request

router = APIRouter(prefix="/issues", tags=["issues"])


def _ai_client() -> AIClient:
    return AIClient(settings.ai_service_url)


@router.get("")
def list_issues(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    rows = db.query(IssueDraft).filter(IssueDraft.user_id == current_user.id).order_by(IssueDraft.created_at.desc()).all()
    return {
        "success": True,
        "data": [
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "sourceType": r.source_type,
                "priority": r.priority,
                "status": r.status.value,
                "aiStatus": r.ai_status,
            }
            for r in rows
        ],
    }


@router.post("/import")
def import_issue(payload: IssueImportRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = IssueDraft(
        user_id=current_user.id,
        title=payload.title,
        description=payload.description,
        source_type=payload.sourceType,
        priority=payload.priority,
        status=DraftStatus.DRAFT,
        ai_status="TBD",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {
        "success": True,
        "message": "Issue draft created",
        "data": {
            "id": row.id,
            "title": row.title,
            "description": row.description,
            "sourceType": row.source_type,
            "status": row.status.value,
            "aiStatus": row.ai_status,
        },
    }


@router.get("/drafts")
def list_drafts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    rows = db.query(IssueDraft).filter(IssueDraft.user_id == current_user.id).order_by(IssueDraft.created_at.desc()).all()
    return {"success": True, "data": rows and [
        {
            "id": r.id,
            "title": r.title,
            "priority": r.priority,
            "status": r.status.value,
            "aiStatus": r.ai_status,
        }
        for r in rows
    ] or []}


@router.get("/{issue_id}")
def get_issue(issue_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(IssueDraft).filter(IssueDraft.id == issue_id, IssueDraft.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Issue not found")
    return {
        "success": True,
        "data": {
            "id": row.id,
            "title": row.title,
            "description": row.description,
            "priority": row.priority,
            "status": row.status.value,
            "aiStatus": row.ai_status,
        },
    }


@router.post("/{issue_id}/send-to-approval")
def send_to_approval(issue_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(IssueDraft).filter(IssueDraft.id == issue_id, IssueDraft.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Issue not found")
    row.status = DraftStatus.SENT_TO_APPROVAL
    approval = ApprovalRequest(user_id=current_user.id, issue_draft_id=row.id, type="CREATE_ISSUE")
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return {"success": True, "message": "Issue sent to approval", "data": {"approvalId": approval.id, "status": approval.status.value}}


@router.post("/{issue_id}/analyze")
async def analyze_issue(issue_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(IssueDraft).filter(IssueDraft.id == issue_id, IssueDraft.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Issue not found")

    start = perf_counter()
    result = await _ai_client().safe_post(
        "/issue/generate",
        {
            "rawTitle": row.title,
            "rawDescription": row.description,
            "businessGoal": "",
            "projectContext": "",
            "preferredIssueType": "Story",
            "preferredPriority": row.priority,
        },
    )
    if result.get("success") and result.get("data"):
        data = result["data"]
        db.add(
            IssueAnalysis(
                issue_draft_id=row.id,
                generated_title=data.get("title", row.title),
                generated_description=data.get("description", row.description),
                issue_type=data.get("issueType", "Story"),
                priority=data.get("priority", row.priority),
                labels=data.get("labels", []),
                acceptance_criteria=data.get("acceptanceCriteria", []),
                suggested_subtasks=data.get("suggestedSubtasks", []),
                confidence=data.get("confidence", 0.0),
            )
        )
    row.ai_status = "DONE" if result.get("success") else "FAILED"
    db.commit()
    log_ai_request(
        db,
        user_id=current_user.id,
        route="/issue/generate",
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status="SUCCESS" if result.get("success") else "FAILED",
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get("message") if not result.get("success") else None,
    )
    return result


@router.post("/{issue_id}/quality-score")
async def issue_quality_score(issue_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(IssueDraft).filter(IssueDraft.id == issue_id, IssueDraft.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Issue not found")

    start = perf_counter()
    result = await _ai_client().safe_post(
        "/issue/quality-score",
        {
            "title": row.title,
            "description": row.description,
            "acceptanceCriteria": [],
            "issueType": "Task",
            "priority": row.priority,
            "labels": [],
        },
    )
    if result.get("success") and result.get("data"):
        data = result["data"]
        db.add(
            IssueQualityScore(
                issue_draft_id=row.id,
                overall_score=data.get("overallScore", 0),
                clarity_score=data.get("clarityScore", 0),
                completeness_score=data.get("completenessScore", 0),
                testability_score=data.get("testabilityScore", 0),
                dependency_clarity_score=data.get("dependencyClarityScore", 0),
                business_value_score=data.get("businessValueScore", 0),
                problems=data.get("problems", []),
                recommendations=data.get("recommendations", []),
                confidence=data.get("confidence", 0.0),
            )
        )
        db.commit()
    log_ai_request(
        db,
        user_id=current_user.id,
        route="/issue/quality-score",
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status="SUCCESS" if result.get("success") else "FAILED",
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get("message") if not result.get("success") else None,
    )
    return result


@router.post("/{issue_id}/business-impact")
async def issue_business_impact(issue_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(IssueDraft).filter(IssueDraft.id == issue_id, IssueDraft.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Issue not found")

    start = perf_counter()
    result = await _ai_client().safe_post(
        "/business/impact-score",
        {
            "title": row.title,
            "description": row.description,
            "priority": row.priority,
            "customerFacing": True,
            "releaseCritical": False,
            "blocked": False,
            "delayRisk": "Medium",
        },
    )
    if result.get("success") and result.get("data"):
        data = result["data"]
        db.add(
            BusinessImpactScore(
                issue_draft_id=row.id,
                impact_level=data.get("impactLevel", "Low"),
                impact_score=data.get("impactScore", 0),
                cost_of_delay=data.get("costOfDelay", "Low"),
                customer_impact=data.get("customerImpact", "Low"),
                release_risk=data.get("releaseRisk", "Low"),
                reasoning=data.get("reasoning", []),
                recommended_action=data.get("recommendedAction", []),
                confidence=data.get("confidence", 0.0),
            )
        )
        db.commit()
    log_ai_request(
        db,
        user_id=current_user.id,
        route="/business/impact-score",
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status="SUCCESS" if result.get("success") else "FAILED",
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get("message") if not result.get("success") else None,
    )
    return result


@router.post("/{issue_id}/generate-recommendations")
async def generate_recommendations(issue_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(IssueDraft).filter(IssueDraft.id == issue_id, IssueDraft.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Issue not found")

    start = perf_counter()
    result = await _ai_client().safe_post(
        "/explain",
        {
            "scoreType": "ISSUE_QUALITY",
            "score": 60,
            "riskLevel": "Medium",
            "factors": [
                "Issue draft requires AI enrichment",
                "Additional acceptance criteria improve implementation accuracy",
            ],
        },
    )
    if result.get("success") and result.get("data"):
        data = result["data"]
        db.add(
            AIRecommendation(
                issue_draft_id=row.id,
                recommendation_type="EXPLANATION",
                title="AI Recommendation",
                description=data.get("summary", "No summary provided"),
                reason="Generated by explainability API.",
                status="ACTIVE",
                confidence=1.0,
            )
        )
        db.commit()
    log_ai_request(
        db,
        user_id=current_user.id,
        route="/explain",
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status="SUCCESS" if result.get("success") else "FAILED",
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get("message") if not result.get("success") else None,
    )
    return result
