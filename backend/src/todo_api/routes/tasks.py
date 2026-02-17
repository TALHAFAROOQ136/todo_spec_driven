import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.auth import get_current_user_id
from todo_api.db import get_session
from todo_api.models import (
    Task,
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
    MessageResponse,
)

router = APIRouter(prefix="/api", tags=["Tasks"])


def _verify_user(path_user_id: str, jwt_user_id: str) -> None:
    if path_user_id != jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user",
        )


def _task_to_response(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


# --- POST: Create task ---


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    user_id: str,
    body: TaskCreate,
    jwt_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    _verify_user(user_id, jwt_user_id)
    task = Task(
        title=body.title.strip(),
        description=body.description,
        user_id=jwt_user_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return _task_to_response(task)


# --- GET: List all tasks ---


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def list_tasks(
    user_id: str,
    jwt_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskListResponse:
    _verify_user(user_id, jwt_user_id)
    result = await session.exec(
        select(Task).where(Task.user_id == jwt_user_id)
    )
    tasks = result.all()
    return TaskListResponse(tasks=[_task_to_response(t) for t in tasks])


# --- GET: Single task ---


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: uuid.UUID,
    jwt_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    _verify_user(user_id, jwt_user_id)
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != jwt_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return _task_to_response(task)


# --- PUT: Update task ---


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: uuid.UUID,
    body: TaskUpdate,
    jwt_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    _verify_user(user_id, jwt_user_id)
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != jwt_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    task.title = body.title.strip()
    task.description = body.description
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return _task_to_response(task)


# --- PATCH: Toggle completion ---


@router.patch(
    "/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse
)
async def toggle_task_complete(
    user_id: str,
    task_id: uuid.UUID,
    jwt_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    _verify_user(user_id, jwt_user_id)
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != jwt_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    task.completed = not task.completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return _task_to_response(task)


# --- DELETE: Remove task ---


@router.delete("/{user_id}/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    user_id: str,
    task_id: uuid.UUID,
    jwt_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> MessageResponse:
    _verify_user(user_id, jwt_user_id)
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != jwt_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    await session.delete(task)
    await session.commit()
    return MessageResponse(message="Task deleted successfully")
