class ApprovalService:
    def submit(self, issue_id: str, approve: bool) -> dict:
        status = "approved" if approve else "rejected"
        return {"issue_id": issue_id, "status": status}
