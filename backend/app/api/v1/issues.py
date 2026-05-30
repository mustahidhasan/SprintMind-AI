from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.entities import ApprovalRequest, DraftStatus, IssueDraft, User
from app.schemas.issue import IssueImportRequest

router = APIRouter(prefix="/issues", tags=["issues"])


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
