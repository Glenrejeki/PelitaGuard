from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.domain_models import User
from app.schemas.auth_schemas import UserCreate, Token, UserLogin

router = APIRouter()

@router.post("/register", response_model=Token)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    try:
        # 1. Cek apakah email sudah ada
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Email sudah terdaftar.",
            )

        # 2. Cek apakah username sudah ada
        user = db.query(User).filter(User.username == user_in.username).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Username sudah digunakan.",
            )

        # 3. Buat user baru
        db_obj = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=security.get_password_hash(user_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": security.create_access_token(
                db_obj.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    except Exception as e:
        # Print error ke terminal backend agar kita bisa baca
        print(f"DATABASE ERROR: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan pada database: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(
    *,
    db: Session = Depends(get_db),
    user_in: UserLogin
) -> Any:
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not security.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Username atau password salah")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
