from fastapi import FastAPI, Depends, Body
from database import *
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models import *

Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do_API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {"message": "Hello!"}


@app.get("/api/task")
async def get_tasks(db: Session = Depends(get_db)) -> list[TaskModel]:
    tasks = db.query(Task).all()
    tasks_with_status = []
    for item in tasks:
        status = db.query(Status).get(item.status_id)
        task = TaskModel(id=item.id, name=item.name, desc=item.desc,
                         create_time=item.create_time, update_time=item.update_time,
                         status=StatusModel(id=item.status_id, name=status.name_status))
        tasks_with_status.append(task)
    return tasks_with_status


@app.get("/api/task/{id}")
async def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        return JSONResponse(status_code=404, content={"message": "Нет такой задачи"})
    else:
        status = db.query(Status).get(task.status_id)
        task = TaskModel(id=task.id, name=task.name, desc=task.desc,
                         create_time=task.create_time, update_time=task.update_time,
                         status=StatusModel(id=task.status_id, name=status.name_status))
        return task


@app.post('/api/task')
async def create_task(data=Body(), db: Session = Depends(get_db), ):
    task = Task(name=data["name"], desc=data["desc"],
                status_id=data["status_id"])
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
