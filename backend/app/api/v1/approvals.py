from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.entities import ApprovalRequest, ApprovalStatus, DraftStatus, IssueDraft, User

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("")
def list_approvals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    rows = (
        db.query(ApprovalRequest)
        .filter(ApprovalRequest.user_id == current_user.id)
        .order_by(ApprovalRequest.created_at.desc())
        .all()
    )
    return {
        "success": True,
        "data": [
            {
                "id": r.id,
                "issueDraftId": r.issue_draft_id,
                "type": r.type,
                "status": r.status.value,
            }
            for r in rows
        ],
    }


@router.post("/{approval_id}/approve")
def approve(approval_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id, ApprovalRequest.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Approval not found")
    row.status = ApprovalStatus.APPROVED
    draft = db.query(IssueDraft).filter(IssueDraft.id == row.issue_draft_id).first()
    if draft:
        draft.status = DraftStatus.APPROVED
    db.commit()
    return {"success": True, "message": "Approved", "data": {"id": row.id, "status": row.status.value}}


@router.post("/{approval_id}/reject")
def reject(approval_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    row = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id, ApprovalRequest.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Approval not found")
    row.status = ApprovalStatus.REJECTED
    draft = db.query(IssueDraft).filter(IssueDraft.id == row.issue_draft_id).first()
    if draft:
        draft.status = DraftStatus.REJECTED
    db.commit()
    return {"success": True, "message": "Rejected", "data": {"id": row.id, "status": row.status.value}}
