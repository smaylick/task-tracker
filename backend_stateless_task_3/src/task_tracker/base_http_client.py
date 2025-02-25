import requests
from abc import ABC, abstractmethod

class BaseHTTPClient(ABC):
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {}

    def get(self, endpoint=""):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def post(self, endpoint="", data=None, json_data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, data=data, json=json_data)
        return self._handle_response(response)

    def put(self, endpoint="", data=None, json_data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, data=data, json=json_data)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except Exception:
                return response.text
        else:
            self.handle_error(response)

    @abstractmethod
    def handle_error(self, response):
        """Метод обработки ошибок – реализуйте в классах-наследниках"""
        pass