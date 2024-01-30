from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime


SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, index=True)
    name_status = Column(String(20))
    tasks = relationship("Task", backref="status")


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    desc = Column(Text, nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status_id = Column(Integer, ForeignKey('status.id'))


SessionLocal = sessionmaker(autoflush=False, bind=engine)
