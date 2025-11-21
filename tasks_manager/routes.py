from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from auth.dependencies import get_current_user

from .schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from .services import (
    create_task_service,
    get_tasks_service,
    update_task_service,
    delete_task_service
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ------------------------------
# CREATE TASK
# ------------------------------
@router.post("/", response_model=TaskResponseSchema)
async def create_task(
    payload: TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await create_task_service(payload, user.id, db)


# ------------------------------
# VIEW USER TASKS
# ------------------------------
@router.get("/", response_model=list[TaskResponseSchema])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await get_tasks_service(user.id, db)


# ------------------------------
# UPDATE TASK
# ------------------------------
@router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: int,
    payload: TaskUpdateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await update_task_service(task_id, payload, user.id, db)


# ------------------------------
# DELETE TASK
# ------------------------------
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await delete_task_service(task_id, user.id, db)
