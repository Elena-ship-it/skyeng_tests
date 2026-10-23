from pathlib import Path
import pytest
from dotenv import load_dotenv
from utils.api_client import APIClient

# Загрузка .env файла
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


# ================= Фикстура APIClient ==================
@pytest.fixture(scope="session")
def api_client():
    """
    Фикстура для работы с APIClient
    """
    client = APIClient()  # Использует BASE_API_URL и токен из .env
    return client


# ================= Фикстура для трекинга созданных событий ==================
@pytest.fixture
def created_events_tracker(api_client):
    """
    Хранит ID созданных событий для последующего удаления.
    Автоматически удаляет события после теста.
    """
    tracker = []
    yield tracker

    if tracker:
        print(f">>> Teardown: удаляем события {tracker}")
        for event_id in tracker:
            resp = api_client.delete_event(event_id)

            if isinstance(resp, dict):
                # на случай, если вернулся словарь
                status_code = resp.get("status_code")
                text = resp.get("text", "")
            else:
                status_code = getattr(resp, "status_code", None)
                text = getattr(resp, "text", "")

            if status_code == 200:
                print(f">>> Событие {event_id} удалено")
            else:
                print(
                    f"!!! Не удалось удалить событие {event_id}: "
                    f"{status_code} {text}"
                )
