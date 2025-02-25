import os
import json
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")
JSONBIN_ID = os.getenv("JSONBIN_ID")

HEADERS = {
    "X-Master-Key": JSONBIN_API_KEY,
    "Content-Type": "application/json"
}

BASE_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}"

class TaskStorage:
    """Класс для работы с JSON-хранилищем jsonbin.io"""

    @staticmethod
    def load_tasks():
        """Получить список задач из jsonbin.io"""
        response = requests.get(BASE_URL, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("record", {}).get("tasks", [])  # Загружаем список задач
        print("Ошибка загрузки:", response.status_code, response.text)  # Лог ошибок
        return []

    @staticmethod
    def save_tasks(tasks):
        """Сохранить список задач в jsonbin.io"""
        data = {"tasks": tasks}  # jsonbin.io требует, чтобы данные были внутри "record"
        response = requests.put(BASE_URL, headers=HEADERS, json=data)  # Передаём через `json=`
        if response.status_code == 200:
            return True
        print("Ошибка сохранения:", response.status_code, response.text)  # Лог ошибок
        return False