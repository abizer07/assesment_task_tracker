from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from .models import Task
from .schemas import TaskCreateSchema, TaskUpdateSchema


# ------------------------------
# CREATE TASK
# ------------------------------
async def create_task_service(data: TaskCreateSchema, user_id: int, db: AsyncSession):
    new_task = Task(
        title=data.title,
        completed=data.completed,
        user_id=user_id
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


# ------------------------------
# VIEW ALL TASKS FOR USER
# ------------------------------
async def get_tasks_service(user_id: int, db: AsyncSession):
    stmt = select(Task).where(Task.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# ------------------------------
# UPDATE TASK
# ------------------------------
async def update_task_service(task_id: int, data: TaskUpdateSchema, user_id: int, db: AsyncSession):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(stmt)
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if data.title is not None:
        task.title = data.title
    
    if data.completed is not None:
        task.completed = data.completed

    await db.commit()
    await db.refresh(task)
    return task


# ------------------------------
# DELETE TASK
# ------------------------------
async def delete_task_service(task_id: int, user_id: int, db: AsyncSession):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(stmt)
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted successfully"}
