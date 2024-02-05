from pydantic import BaseModel, field_validator
from datetime import datetime


class StatusModel(BaseModel):
    id: int = None
    name: str = None


class TaskModel(BaseModel):
    id: int
    name: str
    desc: str
    create_time: datetime
    update_time: datetime
    status: StatusModel()


class CreateTaskModel(BaseModel):
    name: str
    desc: str
    status: int
            
    @field_validator('status')
    def validate_status(cls, value):
        if value not in (1, 2, 3, 4):
            raise ValueError('Status must be 1, 2, 3 or 4')
        return value
    