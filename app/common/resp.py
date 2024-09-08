from fastapi import status
from fastapi.responses import JSONResponse  # , ORJSONResponse
from pydantic import BaseModel
from typing import Union, Optional, TypeVar, Generic

from .error_code import ErrorBase

T = TypeVar("T")


class RestfulModel(BaseModel, Generic[T]):
    code: int
    msg: str
    data: T


def Success(data: Union[list, dict, str] = None, msg: str = "Success"):
    """接口成功返回"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=RestfulModel(code=status.HTTP_200_OK, msg=msg, data=data).dict(
            exclude_none=True
        ),
    )


def Error(
    error: ErrorBase,
    *,
    msg: Optional[str] = None,
    msg_append: str = "",
    data: Union[list, dict, str] = None,
):
    """错误接口返回"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=RestfulModel(
            code=error.code, msg=(msg or error.msg) + msg_append, data=data
        ).dict(exclude_none=True),
    )
