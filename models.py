from pydantic import BaseModel
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
