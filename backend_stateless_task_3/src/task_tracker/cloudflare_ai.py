# cloudflare_ai.py
import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

# Загружаем переменные окружения
load_dotenv()

class CloudflareAI(BaseHTTPClient):
    def __init__(self):
        CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
        CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        CLOUDFLARE_MODEL = "@cf/meta/llama-3.1-8b-instruct"
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{CLOUDFLARE_MODEL}"
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }
        super().__init__(base_url, headers)

    def generate_solution(self, task_text):
        data = {
            "prompt": f"Ты — умный ассистент. Опиши пошаговый план решения задачи: '{task_text}'. Дай развернутый ответ."
        }
        response = self.post("", json_data=data)
        try:
            return response["result"]["response"]
        except KeyError:
            raise Exception("Ошибка в ответе Cloudflare AI")

    def handle_error(self, response):
        raise Exception(f"Ошибка Cloudflare AI: {response.status_code} - {response.text}")