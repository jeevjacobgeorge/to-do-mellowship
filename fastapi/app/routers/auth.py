import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import (
    SessionDep, authenticate_user, get_password_hash,
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.db.models import User, UserIn, UserInDB, Token
from sqlmodel import select

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=User)
async def register(user_in: UserIn, session: SessionDep):
    # Check if user already exists in the database
    existing_user = session.exec(
        select(UserInDB).where(UserInDB.username == user_in.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user_in.password)
    
    # Create new user
    user_db = UserInDB(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        disabled=False
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    user = authenticate_user(session, form_data.username, form_data.password)
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