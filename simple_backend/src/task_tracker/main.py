import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

TASKS_FILE = "tasks.json"  # Файл для хранения задач


class Task(BaseModel):
    id: int
    title: str
    status: str


class TaskStorage:
    """Класс для работы с файлом хранения задач"""

    def __init__(self, filename=TASKS_FILE):
        self.filename = filename

    def load_tasks(self):
        """Загружает задачи из JSON-файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task(**task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks):
        """Сохраняет задачи в JSON-файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.dict() for task in tasks], file, indent=4, ensure_ascii=False)


class TaskManager:
    """Класс для управления списком задач"""

    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()
        self.next_id = max((task.id for task in self.tasks), default=0) + 1  # Следующий ID

    def get_tasks(self):
        return self.tasks

    def create_task(self, title, status="в процессе"):
        task = Task(id=self.next_id, title=title, status=status)
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)  # Сохраняем изменения
        return task

    def update_task(self, task_id, title=None, status=None):
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if status:
                    task.status = status
                self.storage.save_tasks(self.tasks)  # Сохраняем изменения
                return task
        raise HTTPException(status_code=404, detail="Задача не найдена")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.storage.save_tasks(self.tasks)  # Сохраняем изменения
                return
        raise HTTPException(status_code=404, detail="Задача не найдена")


# Создаём объект TaskStorage и передаём его в TaskManager
storage = TaskStorage()
task_manager = TaskManager(storage)


@app.get("/tasks")
def get_tasks():
    return task_manager.get_tasks()


@app.post("/tasks")
def create_task(title: str, status: str = "в процессе"):
    return task_manager.create_task(title, status)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, status: str = None):
    return task_manager.update_task(task_id, title, status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_manager.delete_task(task_id)
    return {"message": "Задача удалена"}