# skyeng_tests
## 🔐 Настройка окружения

Перед запуском тестов необходимо создать файл `.env`
в корне проекта.

Обязательные переменные:
- UI_LOGIN
- UI_PASSWORD
- TOKEN_GLOBAL

Пример заполнения см. в файле `.env.example`

Проект предназначен для **UI и API тестирования расписания** на платформе  
**teacher.skyeng.ru** с использованием `pytest`, `selenium` и `requests`.

Тесты покрывают:
- API работы с событиями расписания
- UI-сценарии создания и проверки личных событий преподавателя
- Валидации форм и отображение событий в расписании

---

## 📌 Цель проекта

- Проверка корректности API расписания
- Автоматизация UI-тестов для основных пользовательских сценариев
- Демонстрация навыков работы с:
  - Selenium WebDriver
  - Pytest (markers, fixtures)
  - Page Object Model
  - Allure-отчетами

---

## 🧱 Структура проекта

skyeng_tests/
├── .gitignore
├── .env # Переменные окружения
├── README.md
├── requirements.txt
├── pytest.ini
├── config.py # Общие настройки проекта
├── helper.py # UI helper и базовая логика
├── tests/
│ ├── conftest.py # Фикстуры pytest
│ ├── test_api.py # API тесты
│ ├── test_api_events.py
│ ├── test_ui.py # UI тесты
│ └── init.py
├── utils/
│ ├── api_client.py # API клиент
│ ├── schedule_api.py # API расписания
│ ├── ui_driver.py # WebDriver
│ └── init.py
├── pages/
│ ├── personal_event_page.py # Page Object
│ └── init.py

yaml
Копировать код

---

## ⚙️ Зависимости

Используемые библиотеки:

- `selenium`
- `requests`
- `pytest`
- `allure-pytest`

Все зависимости указаны в файле `requirements.txt`.

---

## 🚀 Установка и запуск

### 1️⃣ Клонировать репозиторий

```bash
git clone <URL_репозитория>
cd skyeng_tests
2️⃣ Настроить окружение
Скопировать файл .env.example (если есть) в .env и заполнить значения:

env
Копировать код
UI_LOGIN=your_login
UI_PASSWORD=your_password
3️⃣ Создать виртуальное окружение и установить зависимости
bash
Копировать код
python -m venv venv
venv\Scripts\activate           # Windows

pip install -r requirements.txt
▶️ Запуск тестов
🔹 Только UI тесты
bash
Копировать код
pytest -m ui
🔹 Только API тесты
bash
Копировать код
pytest -m api
🔹 Все тесты
bash
Копировать код
pytest
📊 Allure отчет
Запуск тестов с генерацией отчета
bash
Копировать код
pytest -m ui --alluredir=allure-results
pytest -m api --alluredir=allure-results
Просмотр отчета
bash
Копировать код
allure serve allure-results
🔖 Маркеры pytest
@pytest.mark.ui — UI тесты

@pytest.mark.api — API тесты

@pytest.mark.flaky — нестабильные UI сценарии

🔗 Ссылка на финальный проект
👉 GitHub репозиторий:
https://github.com/Elena-ship-it/skyeng_tests.git

🧑‍💻 Автор
Проект выполнен в рамках обучения автоматизации тестирования
(UI + API, Python, Pytest, Selenium).
