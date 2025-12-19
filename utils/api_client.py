import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv


# ================== Загрузка .env ==================
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

BASE_API_URL = os.getenv(
    "BASE_API_URL", "https://api-teachers.skyeng.ru/v2"
)
TOKEN_GLOBAL = os.getenv("TOKEN_GLOBAL")

if not TOKEN_GLOBAL or TOKEN_GLOBAL.strip() == "":
    raise ValueError("❌ TOKEN_GLOBAL отсутствует в .env файле!")

# ВАЖНО: Skyeng НЕ использует Bearer — только чистый токен
AUTH_HEADER = TOKEN_GLOBAL.strip()

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self) -> None:
        self.base_url = BASE_API_URL
        self.headers = {
            "Cookie": AUTH_HEADER,
            "Content-Type": "application/json",
        }
        logger.debug("APIClient токен инициализирован.")

    # ================== Универсальный POST ==================
    def _post(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> Optional[requests.Response]:
        """Универсальный POST-запрос с обработкой ошибок."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            return response

        except Exception as e:
            logger.error(f"API POST error at {endpoint}: {e}")
            return None

    # ================== POST /schedule/createPersonal ==================
    def create_event(
        self, data: Dict[str, Any]
    ) -> Optional[requests.Response]:
        return self._post("/schedule/createPersonal", data)

    # ================== POST /schedule/events ==================
    def list_events(
        self, data: Dict[str, Any]
    ) -> Optional[requests.Response]:
        return self._post("/schedule/events", data)

    # ================== POST /schedule/removePersonal ==================
    def delete_event(
        self, event_id: int
    ) -> Optional[requests.Response]:
        payload = {"id": event_id}
        return self._post("/schedule/removePersonal", payload)
