from fastapi import FastAPI
from app import register, db, routers

# 设置
import sys

sys.dont_write_bytecode = True

# 初始化数据库
db.init_db()

# 实例化 FastAPI 并且配置OpenAPI
app = FastAPI(
    title="FastAPI User Auth Template",
    version="0.1.0",
    contact={
        "name": "Zorn Wang",
        "url": "https://github.com/ZornWang",
        "email": "zornw@foxmail.com",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# 配置路由
app.include_router(routers.api_router, prefix="/api")

# 添加中间件
register.registerMiddlewareHandle(app)
