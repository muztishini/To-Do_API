from fastapi import FastAPI, Depends, HTTPException
from database import *
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models import *
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do_API")

lst = set([1, 2, 3, 4])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {"message": "Hello!"}


@app.get("/api/task", response_model=List[TaskModel])
async def get_tasks(db: Session = Depends(get_db)) -> list[TaskModel]:
    tasks = db.query(Task).all()
    return tasks


@app.get("/api/task/{id}", response_model=TaskModel)
async def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail=f"Задача {id} не найдена")
    else:
        return task


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
