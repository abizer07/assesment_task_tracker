from pydantic import BaseModel

class TaskBaseSchema(BaseModel):
    title: str
    completed: bool = False

class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TaskResponseSchema(TaskBaseSchema):
    id: int
    user_id: int

    class Config:
        from_attributes = True
