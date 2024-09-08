from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from ..common import error_code, Error
from ..dao import user_dao
from ..core import create_access_token, verify_password
from ..schemas import Token, User

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_dao.get_user_by_name(db, form_data.username)
    if user is None:
        return Error(error_code.ERROR_USER_NOT_FOUND)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return Token(access_token=create_access_token(user.username), token_type="bearer")


@router.get("/me", response_model=User, response_model_exclude={"hashed_password"})
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
