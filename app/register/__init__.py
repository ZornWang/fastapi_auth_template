from .middleware import *
from fastapi import FastAPI


def registerMiddlewareHandle(server: FastAPI):
    server.add_middleware(ProcessTimeMiddleware)
    # server.add_middleware(ResponseMiddleware)
