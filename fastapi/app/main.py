from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database import create_db_and_tables
from app.routers import auth, todos

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Todo API")

# Configure CORS
origins = [
    "http://localhost:5173",   # Vite React frontend default port
    "http://127.0.0.1:5173",
    "http://localhost:3000",   # (optional, if using different port)
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Welcome to the Todo API. Visit /docs for documentation"}