from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from redis import Redis
from app import crud, schemas
from app.database import get_db

router = APIRouter()

# Configuração do Redis
redis_client = Redis(host='localhost', port=6379, db=0)

def get_cached_task(task_id: int):
    cached_task = redis_client.get(f"task:{task_id}")
    if cached_task:
        return schemas.Task.parse_raw(cached_task)
    return None

def set_cached_task(task: schemas.Task):
    redis_client.setex(f"task:{task.id}", 3600, task.json())

def invalidate_cache(task_id: int):
    redis_client.delete(f"task:{task_id}")

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.create_task(db=db, task=task)
    task_pydantic = schemas.Task.from_orm(db_task)  # Convertendo para o modelo Pydantic
    set_cached_task(task_pydantic)
    return task_pydantic

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    cached_task = get_cached_task(task_id)
    if cached_task:
        return cached_task
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_pydantic = schemas.Task.from_orm(db_task)  # Convertendo para o modelo Pydantic
    set_cached_task(task_pydantic)
    return task_pydantic

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = crud.update_task(db=db, task=task, task_id=task_id)
    task_pydantic = schemas.Task.from_orm(updated_task)  # Convertendo para o modelo Pydantic
    set_cached_task(task_pydantic)
    return task_pydantic

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db=db, task_id=task_id)
    invalidate_cache(task_id)
    return {"ok": True}