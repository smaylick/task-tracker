from task_storage import TaskStorage

class TaskManager:
    def __init__(self):
        self.tasks = TaskStorage.load_tasks()
        self.next_id = max((task["id"] for task in self.tasks), default=0) + 1

    def get_tasks(self):
        return self.tasks

    def create_task(self, title, status="в процессе"):
        task = {"id": self.next_id, "title": title, "status": status}
        self.tasks.append(task)
        self.next_id += 1
        TaskStorage.save_tasks(self.tasks)
        return task

    def update_task(self, task_id, title=None, status=None):
        for task in self.tasks:
            if task["id"] == task_id:
                if title:
                    task["title"] = title
                if status:
                    task["status"] = status
                TaskStorage.save_tasks(self.tasks)
                return task
        return None

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        TaskStorage.save_tasks(self.tasks)