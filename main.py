from fastapi import FastAPI, Depends, HTTPException
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
async def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    task_models = []
    for task in tasks:
        status = db.query(Status).get(task.status_id)
        task_model = TaskModel(
            id=task.id,
            name=task.name,
            desc=task.desc,
            create_time=task.create_time,
            update_time=task.update_time,
            status=StatusModel(id=status.id, name=status.name_status)
        )
        task_models.append(task_model)

    return task_models


@app.get("/api/task/{id}")
async def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail=f"Задача {id} не найдена")
    else:
        status = db.query(Status).get(task.status_id)
        task_model = TaskModel(
            id=task.id,
            name=task.name,
            desc=task.desc,
            create_time=task.create_time,
            update_time=task.update_time,
            status=StatusModel(id=status.id, name=status.name_status)
        )

        return task_model


@app.post('/api/task')
async def create_task(task: CreateTaskModel,  db: Session = Depends(get_db)):  
    task = Task(name=task.name, desc=task.desc, status_id=task.status)   
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.put("/api/task/{id}")
async def edit_task(task: CreateTaskModel, id: int, db: Session = Depends(get_db)):
    task1 = db.query(Task).filter(Task.id == id).first()
    if not task1:
        raise HTTPException(status_code=404, detail=f"Задача {id} не найдена")
    task1.name = task.name
    task1.desc = task.desc 
    task1.status_id = task.status
          
    db.commit()
    db.refresh(task1)
    return task1


@app.delete("/api/task/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Задача {id} не найдена")
    db.delete(task)
    db.commit()
    return JSONResponse(status_code=200, content={"message": f"Задача {id} удалена"})
