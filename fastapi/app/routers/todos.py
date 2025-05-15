from datetime import datetime
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.dependencies import SessionDep, get_current_active_user
from app.db.models import Todo, TodoCreate, TodoUpdate, UserInDB

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@router.post("/", response_model=Todo)
async def create_todo(
    todo: TodoCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: SessionDep
):
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


@router.get("/", response_model=Dict[str, List[Todo]])
def view_todos(
    session: SessionDep,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    now = datetime.now()
    todos = session.exec(
        select(Todo).where(Todo.owner_username == current_user.username)
    ).all()

    grouped = {
        "to_be_done": [],
        "completed": [],
        "time_elapsed": []
    }

    for todo in todos:
        if todo.completed:
            grouped['completed'].append(todo)
        elif todo.deadline and todo.deadline < now:
            grouped["time_elapsed"].append(todo)
        else:
            grouped["to_be_done"].append(todo)
    return grouped


@router.patch("/{todo_id}/complete", response_model=Todo)
def mark_completed(
    todo_id: int,
    session: SessionDep,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_username != current_user.username:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo.completed = True
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=Todo)
def edit_todo(
    todo_id: int,
    updated: TodoUpdate,
    session: SessionDep,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
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


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    session: SessionDep,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_username != current_user.username:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"detail": "Todo deleted"}