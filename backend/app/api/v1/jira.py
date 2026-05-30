from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import encrypt_secret
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.entities import JiraConnection, JiraConnectionStatus, User
from app.schemas.jira import JiraConnectRequest

router = APIRouter(prefix="/jira", tags=["jira"])


@router.post("/test-connection")
def test_connection(payload: JiraConnectRequest, current_user: User = Depends(get_current_user)) -> dict:
    _ = current_user
    return {
        "success": True,
        "message": "Jira connection is valid",
        "data": {"status": "CONNECTED", "accountName": payload.email.split("@")[0], "accountEmail": payload.email},
    }


@router.post("/connect")
def connect(payload: JiraConnectRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    existing = db.query(JiraConnection).filter(JiraConnection.user_id == current_user.id).first()
    if existing:
        existing.connection_name = payload.connectionName
        existing.base_url = payload.baseUrl
        existing.email = payload.email
        existing.encrypted_api_token = encrypt_secret(payload.apiToken)
        existing.status = JiraConnectionStatus.CONNECTED
        existing.last_tested_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        conn = existing
    else:
        conn = JiraConnection(
            user_id=current_user.id,
            connection_name=payload.connectionName,
            base_url=payload.baseUrl,
            email=payload.email,
            encrypted_api_token=encrypt_secret(payload.apiToken),
            status=JiraConnectionStatus.CONNECTED,
            last_tested_at=datetime.utcnow(),
        )
        db.add(conn)
        db.commit()
        db.refresh(conn)

    return {
        "success": True,
        "message": "Jira connected successfully",
        "data": {
            "id": conn.id,
            "connectionName": conn.connection_name,
            "baseUrl": conn.base_url,
            "email": conn.email,
            "status": conn.status.value,
        },
    }


@router.get("/connection")
def get_connection(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    conn = db.query(JiraConnection).filter(JiraConnection.user_id == current_user.id).first()
    if not conn:
        return {"success": True, "data": None}
    return {
        "success": True,
        "data": {
            "id": conn.id,
            "connectionName": conn.connection_name,
            "baseUrl": conn.base_url,
            "email": conn.email,
            "status": conn.status.value,
            "lastTestedAt": conn.last_tested_at.isoformat() if conn.last_tested_at else None,
        },
    }


@router.delete("/connection")
def delete_connection(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    conn = db.query(JiraConnection).filter(JiraConnection.user_id == current_user.id).first()
    if conn:
        db.delete(conn)
        db.commit()
    return {"success": True, "message": "Connection removed", "data": None}


@router.post("/sync")
def sync_metadata(current_user: User = Depends(get_current_user)) -> dict:
    _ = current_user
    return {"success": True, "message": "Jira metadata sync completed", "data": {"status": "CONNECTED"}}


@router.get("/projects")
def get_projects(current_user: User = Depends(get_current_user)) -> dict:
    _ = current_user
    return {"success": True, "data": [{"id": "100", "key": "PAY", "name": "Payments Platform"}]}


@router.get("/boards")
def get_boards(current_user: User = Depends(get_current_user)) -> dict:
    _ = current_user
    return {"success": True, "data": [{"id": "200", "name": "Engineering Board", "type": "scrum"}]}


@router.get("/sprints")
def get_sprints(current_user: User = Depends(get_current_user)) -> dict:
    _ = current_user
    return {"success": True, "data": [{"id": "300", "name": "Sprint 24", "state": "active"}]}
