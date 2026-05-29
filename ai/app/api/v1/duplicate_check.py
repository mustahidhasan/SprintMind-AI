from fastapi import APIRouter

router = APIRouter(prefix="/issue", tags=["issue"])


@router.post("/duplicate-check")
def duplicate_check() -> dict:
    return {"duplicate": False, "similar_issue_id": None}
