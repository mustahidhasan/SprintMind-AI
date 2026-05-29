from pydantic import BaseModel


class ApprovalRequestPayload(BaseModel):
    issue_id: str
    approve: bool
