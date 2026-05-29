class AuditService:
    def log_event(self, action: str) -> dict:
        return {"logged": True, "action": action}
