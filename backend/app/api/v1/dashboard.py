from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.entities import ApprovalRequest, ApprovalStatus, IssueDraft, User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    total_issues = db.query(IssueDraft).filter(IssueDraft.user_id == current_user.id).count()
    pending = (
        db.query(ApprovalRequest)
        .filter(ApprovalRequest.user_id == current_user.id, ApprovalRequest.status == ApprovalStatus.PENDING)
        .count()
    )
    return {
        "success": True,
        "data": {
            "totalIssues": total_issues,
            "highRiskIssues": 0,
            "averageQualityScore": 0,
            "pendingApprovals": pending,
            "sprintRisk": "TBD",
            "businessImpact": "TBD",
            "aiStatus": "TBD",
        },
    }
