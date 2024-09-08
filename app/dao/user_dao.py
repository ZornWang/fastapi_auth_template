from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def count_user(db: Session):
    return db.query(User).count()


def get_all_user(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit)


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        hashed_password=user.password,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def promote_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.is_superuser = True
    db.commit()
    db.refresh(db_user)
    return db_user


def demote_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.is_superuser = False
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.username = user.username if user.username else db_user.username
    db_user.hashed_password = (
        user.password if user.password else db_user.hashed_password
    )
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db.delete(db.query(User).filter(User.id == user_id).first())
    db.commit()
    return True
