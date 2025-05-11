from datetime import datetime, timedelta, timezone
from typing import Annotated,Optional

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import urllib
from sqlmodel import Session, SQLModel, create_engine,select,Field,Relationship
from jwt import PyJWTError
from fastapi.middleware.cors import CORSMiddleware

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "b0018fa2a0d50c914744f68c3bf2e979c1bb98e294e3201775cbca3db6114c1c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(SQLModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserIn(User):
    password:str

class UserInDB(User,table=True):
    username:str = Field(primary_key=True)
    hashed_password: str
    todos:list["Todo"] = Relationship(back_populates="owner")
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime

class Todo(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    title:str
    description:Optional[str] = None
    deadline:datetime | None = None
    completed:bool = False
    owner_username: str = Field(foreign_key="userindb.username")
    owner: Optional["UserInDB"] = Relationship(back_populates="todos")
    class Config:
        orm_mode = True
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)


POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = urllib.parse.quote_plus("jeev@123")
POSTGRES_DB = "tododb"
POSTGRES_HOST = "localhost"  # or Docker container name or IP
POSTGRES_PORT = "5432"

postgres_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(postgres_url, echo=True)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()
origins = [
    "http://localhost:5173",   # Vite React frontend default port
    "http://127.0.0.1:5173",
    "http://localhost:3000",   # (optional, if using different port)
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # or ["*"] for public APIs
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)
def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(session:Session, username: str):
    return session.exec(select(UserInDB).where(UserInDB.username==username)).first()


def authenticate_user(session:Session, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except PyJWTError:
        raise credentials_exception
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session:SessionDep
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, username=token_data.username) #here
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/register",response_model=User)
async def register(userin:UserIn,session:SessionDep):
    # Check if user already exists in the database
    existing_user = session.exec(
        select(UserInDB).where(UserInDB.username == userin.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(userin.password)
        # Create new user
    user_db = UserInDB(
        username=userin.username,
        email=userin.email,
        full_name=userin.full_name,
        hashed_password=hashed_password,
        disabled=False
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db



@app.post("/token",response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:SessionDep
):
    user = authenticate_user(session, form_data.username, form_data.password) #here
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")





@app.post('/todos/',response_model=Todo)
async def create_todo(
    todo:TodoCreate,
    current_user: Annotated[UserInDB,Depends(get_current_active_user)],
    session:SessionDep):
        new_todo = Todo(
            title=todo.title,
            description=todo.description,
            deadline=todo.deadline,
            owner_username=current_user.username,
            completed=False
        )
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        return new_todo

# @app.get("/todos/",response_model=list[Todo])
# async def get_my_todo(current_user:Annotated[UserInDB,Depends(get_current_active_user)],session:SessionDep):
#     statement = select(Todo).where(Todo.owner_username == current_user.username)
#     todos = session.exec(statement).all()
#     return todos

@app.get("/todos/")
def view_todos(session:SessionDep,current_user:Annotated[UserInDB,Depends(get_current_active_user)]):
    now = datetime.now()
    todos = session.exec(select(Todo).where(Todo.owner_username == current_user.username)).all()

    grouped = {
        "to_be_done":[],
        "completed":[],
        "time_elapsed":[]
    }

    for todo in todos:
        if todo.completed:
            grouped['completed'].append(todo)
        elif todo.deadline < now:
            grouped["time_elapsed"].append(todo)
        else:
            grouped["to_be_done"].append(todo)
    return grouped

@app.patch('/todos/{todo_id}/complete',response_model=Todo)
def mark_completed(todo_id:int,session:SessionDep,current_user:Annotated[UserInDB,Depends(get_current_active_user)]):
    todo = session.get(Todo,todo_id)
    if not todo or todo.owner_username != current_user.username:
        raise HTTPException(status_code=404,detail='Todo not found')
    todo.completed = True
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def edit_todo(todo_id: int, updated: TodoUpdate, session: SessionDep, current_user: Annotated[UserInDB, Depends(get_current_active_user)]):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_username != current_user.username:
        raise HTTPException(status_code=404, detail="Todo not found")

    if updated.title is not None:
        todo.title = updated.title
    if updated.description is not None:
        todo.description = updated.description
    if updated.deadline is not None:
        todo.deadline = updated.deadline
    if updated.completed is not None:
        todo.completed = updated.completed

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep, current_user: Annotated[UserInDB, Depends(get_current_active_user)]):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_username != current_user.username:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"detail": "Todo deleted"}


         