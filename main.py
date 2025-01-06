from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Setup
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Pydantic Models
class TodoItem(BaseModel):
    title: str
    description: str | None = None

class TodoInResponse(TodoItem):
    id: int

# SQLAlchemy Model
class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

# CRUD operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/todos/", response_model=TodoInResponse)
def create_todo(todo: TodoItem, db: SessionLocal = next(get_db())):
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoInResponse])
def get_todos(db: SessionLocal = next(get_db())):
    return db.query(Todo).all()

@app.put("/todos/{todo_id}", response_model=TodoInResponse)
def update_todo(todo_id: int, todo: TodoItem, db: SessionLocal = next(get_db())):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoInResponse)
def delete_todo(todo_id: int, db: SessionLocal = next(get_db())):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo
