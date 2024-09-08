from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from .db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from .core import config, security
from .schemas import TokenPayload, User
from .dao import user_dao

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = payload["sub"]
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_dao.get_user_by_name(db, str(token_data))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
