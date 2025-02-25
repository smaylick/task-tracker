# task_manager.py
from fastapi import HTTPException
from task_storage import TaskStorage
from cloudflare_ai import CloudflareAI

class TaskManager:
    def __init__(self):
        self.storage = TaskStorage()
        self.storage.initialize_bin()
        self.tasks = self.storage.load_tasks()
        self.next_id = max((task["id"] for task in self.tasks), default=0) + 1

    def get_tasks(self):
        return self.tasks

    def create_task(self, title, status="в процессе"):
        ai_client = CloudflareAI()
        solution = ai_client.generate_solution(title)  # Получаем решение от AI

        task = {
            "id": self.next_id,
            "title": title,
            "solution": solution,
            "status": status
        }
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)
        return task

    def update_task(self, task_id, title=None, status=None):
        for task in self.tasks:
            if task["id"] == task_id:
                if title:
                    task["title"] = title
                if status:
                    task["status"] = status
                self.storage.save_tasks(self.tasks)
                return task
        return None

    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.storage.save_tasks(self.tasks)
                return {"message": "Задача удалена"}
        raise HTTPException(status_code=404, detail="Задача не найдена")