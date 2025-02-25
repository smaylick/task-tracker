# main.py
from fastapi import FastAPI, HTTPException
from task_manager import TaskManager

app = FastAPI()
task_manager = TaskManager()

@app.get("/tasks")
def get_tasks():
    return task_manager.get_tasks()

@app.post("/tasks")
def create_task(title: str, status: str = "в процессе"):
    return task_manager.create_task(title, status)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, status: str = None):
    task = task_manager.update_task(task_id, title, status)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_manager.delete_task(task_id)
    return {"message": "Задача удалена"}