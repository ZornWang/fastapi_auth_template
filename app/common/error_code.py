from pydantic import BaseModel


class ErrorBase(BaseModel):
    code: int
    msg: str = ""


# 找不到路径
ERROR_NOT_FOUND = ErrorBase(code=404, msg="api 路径错误")
# 参数错误
ERROR_PARAMETER_ERROR = ErrorBase(code=400, msg="参数错误")

# 用户相关
# 用户不存在
ERROR_USER_NOT_FOUND = ErrorBase(code=1001, msg="用户不存在")
# 用户已存在
ERROR_USER_EXIST = ErrorBase(code=1002, msg="用户已存在")
# 密码错误
ERROR_PASSWORD_WRONG = ErrorBase(code=1003, msg="密码错误")
# 不允许删除超级用户
ERROR_NOT_ALLOW_DELETE_SUPER_USER = ErrorBase(
    code=1004, msg="当前权限不允许删除超级用户"
)
# 用户已是超级用户
ERROR_USER_IS_SUPER_USER = ErrorBase(code=1005, msg="用户已是超级用户")
# 用户等级已是最低
ERROR_USER_LEVEL_LOWEST = ErrorBase(code=1006, msg="用户等级已是最低")
