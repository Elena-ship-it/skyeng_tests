from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


class PersonalEventPage:
    # -------------------------- Локаторы --------------------------
    PERSONAL_EVENT_TAB = (
        By.XPATH,
        "//sky-ui-tab[contains(., 'Личное событие')]",
    )

    # Слот события – личное событие (реальный DOM)
    EVENT_SLOT = (
        By.CSS_SELECTOR,
        "tcc-calendar-event-personal .long-view",
    )

    EDIT_BTN = (
        By.XPATH,
        "//button[.//div[contains(@class,'text-container') "
        "and contains(., 'Редактировать')]]",
    )
    DELETE_BTN = (
        By.XPATH,
        "//button[.//div[contains(@class,'text-container') "
        "and contains(., 'Удалить')]]",
    )
    SAVE_BTN = (
        By.XPATH,
        "//button[.//div[contains(@class,'text-container') "
        "and contains(., 'Cохранить')]]",
    )
    CONFIRM_DELETE_BTN = (
        By.XPATH,
        "//button[contains(normalize-space(),'Да')]",
    )

    TITLE_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder^='Например:']",
    )
    DESCRIPTION_INPUT = (
        By.CSS_SELECTOR,
        "textarea[maxlength='500']",
    )

    # Реальный класс заголовка в слоте
    SLOT_TITLE = (
        By.CSS_SELECTOR,
        ".long-view__title",
    )

    # Описания нет в DOM → всегда будет пустой
    SLOT_DESCRIPTION = None

    # -------------------------- Инициализация --------------------------
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)

    # -------------------------- Utility --------------------------
    def scroll(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )

    def click(self, locator, timeout=None, clickable: bool = True):
        wait = WebDriverWait(
            self.driver,
            timeout or self.wait._timeout,
        )
        try:
            element = wait.until(
                EC.element_to_be_clickable(locator)
                if clickable
                else EC.visibility_of_element_located(locator),
            )
            self.scroll(element)
            try:
                element.click()
            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ):
                self.actions.move_to_element(
                    element,
                ).pause(0.2).click().perform()
            return element
        except TimeoutException as exc:
            message = (
                f"Элемент {locator} не найден "
                "или не кликабелен"
            )
            raise TimeoutException(message) from exc

    def find(self, locator, timeout=None):
        wait = WebDriverWait(
            self.driver,
            timeout or self.wait._timeout,
        )
        return wait.until(
            EC.presence_of_element_located(locator),
        )

    def find_visible(self, locator, timeout=None):
        wait = WebDriverWait(
            self.driver,
            timeout or self.wait._timeout,
        )
        return wait.until(
            EC.visibility_of_element_located(locator),
        )

    def get_input_value(self, locator, timeout=None) -> str:
        element = self.find_visible(locator, timeout)
        return element.get_attribute("value")

    # -------------------- Вкладка «Личное событие» --------------------
    def open_personal_event_tab(self) -> bool:
        try:
            tab = self.wait.until(
                EC.visibility_of_element_located(
                    self.PERSONAL_EVENT_TAB,
                ),
            )
            self.scroll(tab)
            try:
                tab.click()
            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ):
                self.actions.move_to_element(
                    tab,
                ).pause(0.2).click().perform()

            self.wait.until(
                EC.visibility_of_element_located(
                    self.TITLE_INPUT,
                ),
            )
            return True
        except TimeoutException as exc:
            raise AssertionError(
                "Не удалось открыть вкладку Личное событие",
            ) from exc

    # -------------------------- Слоты --------------------------
    def find_and_open_filled_event(self, timeout: int = 15) -> bool:
        try:
            slot = WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.visibility_of_element_located(
                    self.EVENT_SLOT,
                ),
            )
            self.scroll(slot)
            try:
                slot.click()
            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ):
                self.actions.move_to_element(
                    slot,
                ).pause(0.2).click().perform()

            self.wait.until(
                EC.visibility_of_element_located(
                    self.EDIT_BTN,
                ),
            )
            return True
        except TimeoutException as exc:
            raise AssertionError(
                "Не удалось найти и открыть заполненное событие",
            ) from exc

    # -------------------------- Редактирование --------------------------
    def open_edit_form(self):
        return self.click(self.EDIT_BTN)

    def fill_event_form(self, title: str = "", description: str = ""):
        title_input = self.find_visible(self.TITLE_INPUT)
        self.scroll(title_input)
        title_input.clear()
        title_input.send_keys(title)

        desc_input = self.find_visible(self.DESCRIPTION_INPUT)
        self.scroll(desc_input)
        desc_input.clear()
        desc_input.send_keys(description)

    def save_event(self):
        self.click(self.SAVE_BTN)
        self.wait.until(
            EC.invisibility_of_element_located(
                self.SAVE_BTN,
            ),
        )

    # --------------------- Получение данных слота ---------------------
    def get_event_slot_text(self):
        """Возвращает текст заголовка (описание в DOM отсутствует)."""
        slot = self.find_visible(self.EVENT_SLOT)

        title = slot.find_element(
            *self.SLOT_TITLE,
        ).text.strip()

        description = ""
        return title, description

    # -------------------------- Удаление --------------------------
    def delete_event(self):
        self.click(self.DELETE_BTN)
        try:
            self.click(self.CONFIRM_DELETE_BTN)
        except TimeoutException:
            pass
