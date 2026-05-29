from fastapi import APIRouter

from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])
service = ReportService()


@router.get("/sprint-health")
def sprint_health_report() -> dict:
    return service.sprint_health()
