import os
from dotenv import load_dotenv

load_dotenv()

UI_LOGIN = os.getenv("UI_LOGIN")
UI_PASSWORD = os.getenv("UI_PASSWORD")
BASE_UI_URL = os.getenv("BASE_UI_URL")
SCHEDULE_URL = os.getenv("SCHEDULE_URL")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 50))
HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
BROWSER = os.getenv("BROWSER", "chrome")
