from database import *
from sqlalchemy.orm import Session

with Session(autoflush=False, bind=engine) as db:
    task = db.query(Task).all()

    for t in task:
        print(t.id, t.name)