# app/api.py
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from task_manager import TaskManager

app = FastAPI()
task_manager = TaskManager()
task_manager.setup()

class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    created_at: datetime
    completed: bool

@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    return task_manager.create_task(
        title=task.title,
        description=task.description,
        deadline=task.deadline
    )

@app.get("/tasks/", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = None, before_deadline: Optional[datetime] = None):
    tasks = task_manager.list_tasks()
    
    if status:
        tasks = [t for t in tasks if (t.completed and status == "completed") or 
                                   (not t.completed and status == "pending")]
    
    if before_deadline:
        tasks = [t for t in tasks if t.deadline <= before_deadline]
    
    return tasks

@app.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    if task_manager.mark_task_complete(task_id):
        return {"message": "Task marked as complete"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task_manager.delete_task(task_id)
    return {"message": "Task deleted"}