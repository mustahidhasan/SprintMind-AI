from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.entities import JiraConnection, RefreshToken, User
from app.schemas.auth import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


def ensure_default_admin(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@gmail.com").first()
    if not admin:
        db.add(
            User(
                name="Admin",
                email="admin@gmail.com",
                password_hash=hash_password("admin@gmail.com"),
            )
        )
        db.commit()


@router.post("/register")
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)) -> dict:
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(name=payload.name, email=payload.email.lower(), password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)
    refresh_token, expires_at = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token_hash=hash_refresh_token(refresh_token), expires_at=expires_at))
    db.commit()

    response.set_cookie("refreshToken", refresh_token, httponly=True, samesite="lax")

    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "accessToken": access_token,
            "refreshToken": refresh_token,
        },
    }


@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> dict:
    ensure_default_admin(db)
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token, expires_at = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token_hash=hash_refresh_token(refresh_token), expires_at=expires_at))
    db.commit()

    response.set_cookie("refreshToken", refresh_token, httponly=True, samesite="lax")

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "accessToken": access_token,
            "refreshToken": refresh_token,
        },
    }


@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)) -> dict:
    refresh_token = request.cookies.get("refreshToken")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    token_hash = hash_refresh_token(refresh_token)
    token_row = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if not token_row or token_row.revoked_at or token_row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(token_row.user_id)
    new_refresh, expires_at = create_refresh_token(token_row.user_id)
    token_row.revoked_at = datetime.utcnow()
    db.add(RefreshToken(user_id=token_row.user_id, token_hash=hash_refresh_token(new_refresh), expires_at=expires_at))
    db.commit()

    response.set_cookie("refreshToken", new_refresh, httponly=True, samesite="lax")
    return {"success": True, "message": "Token refreshed", "data": {"accessToken": access_token, "refreshToken": new_refresh}}


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> dict:
    refresh_token = request.cookies.get("refreshToken")
    if refresh_token:
        token_hash = hash_refresh_token(refresh_token)
        token_row = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
        if token_row:
            token_row.revoked_at = datetime.utcnow()
            db.commit()
    response.delete_cookie("refreshToken")
    return {"success": True, "message": "Logout successful", "data": None}


@router.get("/me")
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    has_jira = db.query(JiraConnection).filter(JiraConnection.user_id == current_user.id).first() is not None
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "hasJiraConnection": has_jira,
        },
    }
