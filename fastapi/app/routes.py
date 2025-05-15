# app/routes.py

from fastapi import FastAPI
from app.routers import auth, todos

def include_routes(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(todos.router)
