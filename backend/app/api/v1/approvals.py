from fastapi import APIRouter

from app.schemas.approval import ApprovalRequestPayload
from app.services.approval_service import ApprovalService

router = APIRouter(prefix="/approvals", tags=["approvals"])
service = ApprovalService()


@router.post("")
def submit_approval(payload: ApprovalRequestPayload) -> dict:
    return service.submit(payload.issue_id, payload.approve)
