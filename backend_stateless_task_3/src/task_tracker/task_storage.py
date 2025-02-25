# task_storage.py
import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

# Загружаем переменные окружения
load_dotenv()

class TaskStorage(BaseHTTPClient):
    def __init__(self):
        JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")
        JSONBIN_ID = os.getenv("JSONBIN_ID")
        base_url = f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}"
        headers = {
            "X-Master-Key": JSONBIN_API_KEY,
            "Content-Type": "application/json"
        }
        super().__init__(base_url, headers)

    def initialize_bin(self):
        response = self.get()
        record = response.get("record", {})
        if "tasks" not in record:
            self.save_tasks([])  # Создаем пустой список задач

    def load_tasks(self):
        response = self.get()
        tasks = response.get("record", {}).get("tasks", [])
        return tasks

    def save_tasks(self, tasks):
        data = {"record": {"tasks": tasks}}
        response = self.put("", json_data=data)
        if response:
            return True
        print("Ошибка сохранения данных.")
        return False

    def handle_error(self, response):
        raise Exception(f"Ошибка JSONBin: {response.status_code} - {response.text}")