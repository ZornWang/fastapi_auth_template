from pydantic import BaseModel


class UserBase(BaseModel):
    is_superuser: bool = False


class User(UserBase):
    id: int
    username: str

    # hashed_password: str

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserCreate):
    pass
