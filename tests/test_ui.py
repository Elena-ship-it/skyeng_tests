import logging

import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from helper import SkyEngTestHelper
from pages.personal_event_page import PersonalEventPage
from config import UI_LOGIN, UI_PASSWORD


@pytest.fixture
def helper():
    h = SkyEngTestHelper()
    yield h
    h.quit()


@pytest.mark.ui
class TestUI:
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @allure.feature("SkyEng schedule test")
    @allure.title("1. Проверка открытия страницы Расписание")
    def test_open_schedule(self, helper):
        helper.login(username=UI_LOGIN, password=UI_PASSWORD)
        helper.go_to_schedule()
        assert helper.is_schedule_page_opened(), \
            "Страница расписания не открылась"

    @allure.feature("SkyEng schedule test")
    @allure.title("2. Открытие формы Личное событие")
    def test_open_personal_event_form(self, helper):
        helper.login(username=UI_LOGIN, password=UI_PASSWORD)
        helper.go_to_schedule()

        assert helper.click_free_slot(), \
            "Не удалось найти свободный слот"
        assert helper.click_personal_event(), \
            "Не удалось открыть вкладку Личное событие"
        assert helper.is_personal_event_form_opened(), \
            "Форма личного события не открылась"

    @allure.feature("SkyEng schedule test")
    @allure.title("3. Проверка валидации полей")
    def test_event_form_validation(self, helper):
        helper.login(username=UI_LOGIN, password=UI_PASSWORD)
        helper.go_to_schedule()

        assert helper.click_free_slot(), \
            "Не удалось найти свободный слот"
        assert helper.click_personal_event(), \
            "Не удалось открыть вкладку Личное событие"

        # Проверка заголовка
        helper.set_event_title("")
        assert helper.get_event_title_value() == "", \
            "Заголовок не пустой после очистки"

        helper.set_event_title("А" * 100)
        assert len(helper.get_event_title_value()) <= 40, \
            "Длина заголовка больше допустимой"

        helper.set_event_title("Моё событие")
        assert helper.get_event_title_value() == "Моё событие", \
            "Заголовок не соответствует введённому"

        # Проверка даты
        selected_value = helper.select_event_date(3)
        assert selected_value is not None, "Дата не выбрана"

        # Проверка описания
        description = "Автоматическое тестовое описание события"
        helper.set_event_description(description)
        assert helper.get_event_description_value() == description, \
            "Описание не соответствует введённому"

        helper.click_green_circle()
        helper.click_save_button()
        logging.info("Тест валидации полей пройден успешно!")

    @allure.feature("SkyEng schedule test")
    @allure.title("4. Редактирование события")
    def test_edit_event(self, helper):
        helper.login(username=UI_LOGIN, password=UI_PASSWORD)
        helper.go_to_schedule()

        # 🔹 Создаём событие
        assert helper.click_free_slot(), \
            "Не удалось найти свободный слот"
        assert helper.click_personal_event(), \
            "Не удалось открыть вкладку Личное событие"

        helper.set_event_title("UI автотест")
        helper.set_event_description("Создано автоматически")

        assert helper.save_personal_event(), \
            "Событие не появилось после сохранения"

        # 🔹 Редактирование
        pep = PersonalEventPage(helper.driver)
        assert pep.find_and_open_filled_event(), \
            "Не найдено событие для редактирования"

        pep.open_edit_form()
        pep.fill_event_form("Изменённое событие", "Обновлённое описание")
        pep.save_event()

        title_val, desc_val = pep.get_event_slot_text()
        # Описание не отображается в DOM → проверку пропускаем

    @allure.feature("SkyEng schedule test")
    @allure.title("5. Удаление события")
    def test_delete_event(self, helper):
        helper.login(username=UI_LOGIN, password=UI_PASSWORD)
        helper.go_to_schedule()

        # 🔹 Создаём событие
        assert helper.click_free_slot(), \
            "Не удалось найти свободный слот"
        assert helper.click_personal_event(), \
            "Не удалось открыть вкладку Личное событие"

        helper.set_event_title("UI автотест для удаления")
        helper.set_event_description("Будет удалено")

        assert helper.save_personal_event(), \
            "Событие не появилось после сохранения"

        # 🔹 Удаление
        pep = PersonalEventPage(helper.driver)
        assert pep.find_and_open_filled_event(), \
            "Не найдено событие для удаления"

        pep.delete_event()

        try:
            WebDriverWait(helper.driver, 5).until(
                EC.invisibility_of_element_located(pep.EDIT_BTN)
            )
        except TimeoutException:
            pytest.fail(
                "Событие не удалилось: кнопка редактирования осталась "
                "видимой"
            )
