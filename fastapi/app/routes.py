# app/routes.py

from fastapi import FastAPI
from app.routers import auth, todos, websocket

def include_routes(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(todos.router)
    app.include_router(websocket.router)
