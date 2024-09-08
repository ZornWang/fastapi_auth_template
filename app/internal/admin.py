from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserUpdate, User
from ..dao import user_dao
from ..common import error_code, Success, Error
from ..core import get_password_hash
from ..dependencies import get_db

router = APIRouter()


# 创建用户
@router.post("/", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if user_dao.get_user_by_name(db, user.username):
        return error_code.ERROR_USER_EXIST
    password = get_password_hash(user.password)
    user.password = password
    return user_dao.create_user(db, user)


# 查询所有用户
@router.get("/", response_model=list[User])
async def get_all_user(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    count = user_dao.count_user(db)
    users = user_dao.get_all_user(db, skip, limit)
    return Success(
        {
            "data": [
                User(
                    id=user.id, username=user.username, is_superuser=user.is_superuser
                ).model_dump()
                for user in users
            ],
            "count": count,
        }
    )


# 查询单个用户
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_dao.get_user(db, user_id)
    if user:
        return Success(
            User(
                id=user.id, username=user.username, is_superuser=user.is_superuser
            ).model_dump()
        )
    else:
        return Error(error_code.ERROR_USER_NOT_FOUND)


# 更新用户
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    if user.password:
        user.password = get_password_hash(user.password)
    user_update = user_dao.update_user(db, user_id, user)
    return Success(
        User(
            id=user_update.id,
            username=user_update.username,
            is_superuser=user_update.is_superuser,
        ).model_dump()
    )


# 用户提权
@router.put("/{user_id}/promote", response_model=User)
async def promote_user(user_id: int, db: Session = Depends(get_db)):
    user = user_dao.get_user(db, user_id)
    if user.is_superuser:
        return Error(error_code.ERROR_USER_IS_SUPER_USER)
    user_dao.promote_user(db, user_id)
    return Success(
        User(
            id=user.id,
            username=user.username,
            is_superuser=user.is_superuser,
        ).model_dump()
    )


# 用户降权
@router.put("/{user_id}/demote", response_model=User)
async def demote_user(user_id: int, db: Session = Depends(get_db)):
    user = user_dao.get_user(db, user_id)
    if not user.is_superuser:
        return Error(error_code.ERROR_USER_LEVEL_LOWEST)
    user_dao.demote_user(db, user_id)
    return Success(
        User(
            id=user.id,
            username=user.username,
            is_superuser=user.is_superuser,
        ).model_dump()
    )


# 删除用户
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_dao.get_user(db, user_id)
    if user is None:
        return Error(error_code.ERROR_USER_NOT_FOUND)
    if user.is_superuser:
        return Error(error_code.ERROR_NOT_ALLOW_DELETE_SUPER_USER)
    if user_dao.delete_user(db, user_id):
        return Success()
    else:
        return Error(error_code.ERROR_USER_NOT_FOUND)
