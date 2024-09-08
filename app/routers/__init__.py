from fastapi import APIRouter, Depends

from ..internal import admin
from ..dependencies import get_current_active_superuser
from . import login

api_router = APIRouter()
api_router.include_router(
    admin.router,
    prefix="/user",
    # include_in_schema=False,
    tags=["用户相关"],
    dependencies=[Depends(get_current_active_superuser)],
)
api_router.include_router(login.router, prefix="/login", tags=["登陆相关"])
