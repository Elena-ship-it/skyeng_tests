import logging
import time

import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from config import DEFAULT_TIMEOUT, HEADLESS, SCHEDULE_URL

MAX_RETRY = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def retry(max_runs: int = MAX_RETRY, delay: int = 1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_runs + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    logging.warning(
                        "[Retry] Attempt %s/%s failed: %s",
                        attempt,
                        max_runs,
                        exc,
                    )
                    time.sleep(delay)
            raise last_exc

        return wrapper

    return decorator


class SkyEngTestHelper:
    def __init__(self, driver=None, timeout: int = DEFAULT_TIMEOUT):
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        self.driver = driver or webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        self.wait = WebDriverWait(self.driver, timeout)
        self.actions = ActionChains(self.driver)

    # ---------------- LOGIN ---------------- #
    @allure.step("Login as {username}")
    @retry()
    def login(self, username: str, password: str):
        self.driver.get(
            "https://id.skyeng.ru/login?"
            "redirect=https://teacher.skyeng.ru"
        )
        self.wait.until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete"
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.js-send-otp-form-to-username-password")
            )
        ).click()

        username_input = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        password_input.clear()
        password_input.send_keys(password)

        login_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span.js-username-password-form-button")
            )
        )
        self.actions.move_to_element(login_btn).pause(0.2).click().perform()
        self.wait.until(lambda d: "teacher.skyeng.ru" in d.current_url)

    # ---------------- NAVIGATION ---------------- #
    @allure.step("Navigate to schedule page")
    def go_to_schedule(self):
        self.driver.get(SCHEDULE_URL)
        try:
            schedule_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(), 'Расписание')]")
                )
            )
            self.actions.move_to_element(schedule_btn).pause(0.2).click().perform()
            logging.info("Кнопка 'Расписание' найдена и кликнута")
        except TimeoutException:
            logging.error("Не удалось найти кнопку 'Расписание'")
            raise

    # ---------------- EVENT CREATION ---------------- #
    @allure.step("Click on a free slot")
    def click_free_slot(self) -> bool:
        logging.info("Looking for a free slot...")
        try:
            slot = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.box-hover.hover-enabled")
                )
            )
            self.actions.move_to_element(slot).click().perform()
            return True
        except TimeoutException:
            logging.error("Free slot not found!")
            return False

    @allure.step("Click on personal event '{event_text}'")
    def click_personal_event(self, event_text: str = "Личное событие") -> bool:
        logging.info(f"Looking for personal event: {event_text}")
        try:
            event = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        (
                          "//div[contains(@class,'root')]//*[contains(text(), "
                          f"'{event_text}')]"
                        ),
                    )
                )
            )
            self.actions.move_to_element(event).click().perform()
            return True
        except TimeoutException:
            logging.error(f"Personal event '{event_text}' not found!")
            return False

    # ---------------- EVENT FORM ---------------- #
    @allure.step("Set event title")
    def set_event_title(self, text: str):
        title_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder^='Например:']")
            )
        )
        title_input.clear()
        title_input.send_keys(text)

    def get_event_title_value(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder^='Например:']")
            )
        ).get_attribute("value")

    @allure.step("Set event description")
    def set_event_description(self, text: str):
        textarea = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "textarea[maxlength='500']")
            )
        )
        textarea.clear()
        textarea.send_keys(text)

    def get_event_description_value(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "textarea[maxlength='500']")
            )
        ).get_attribute("value")

    @allure.step("Click green circle")
    def click_green_circle(self):
        svg = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "svg[viewBox='0 0 24 24']")
            )
        )
        self.actions.move_to_element(svg).pause(0.2).click().perform()

    @allure.step("Click Save button")
    def click_save_button(self):
        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    (
                        "//button[.//div[contains(@class,'text-container') "
                        "and contains(., 'Cохранить')]]"
                    ),
                )
            )
        )
        self.actions.move_to_element(save_button).pause(0.2).click().perform()

    # ---------------- SAVE & WAIT ---------------- #
    @allure.step("Save personal event and wait for it to appear")
    def save_personal_event(self) -> bool:
        self.click_save_button()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder^='Например:']")
                )
            )
        except TimeoutException:
            logging.warning("Event form did not close after save")
        return self.wait_for_saved_event()

    # ---------------- EVENT APPEARANCE ---------------- #
    @allure.step("Wait until saved event appears in schedule")
    def wait_for_saved_event(self, timeout: int = 15) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        (
                            "//div[contains(@class,'event') "
                            "and not(contains(@class,'empty'))]"
                        ),
                    )
                )
            )
            logging.info("Saved event appeared in schedule")
            return True
        except TimeoutException:
            logging.error("Saved event did not appear in schedule")
            return False

    # ---------------- VALIDATION ---------------- #
    @allure.step("Select event date")
    def select_event_date(self, days_offset: int = 1) -> str:
        select_elem = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select.class-date"))
        )
        select_obj = Select(select_elem)
        select_obj.select_by_index(days_offset)
        return select_obj.first_selected_option.get_attribute("value")

    # ---------------- CHECKS ---------------- #
    def is_schedule_page_opened(self) -> bool:
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(), 'Расписание')]")
                )
            )
            return True
        except TimeoutException:
            return False

    def is_personal_event_form_opened(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder^='Например:']")
                )
            )
            return True
        except TimeoutException:
            return False

    # ---------------- QUIT ---------------- #
    def quit(self):
        try:
            self.driver.quit()
        except Exception:
            pass
