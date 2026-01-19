from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class LoginPage:
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        """Открыть страницу логина"""
        logger.info("Opening login page")
        self.driver.get("https://www.saucedemo.com/")
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        return self
    
    def enter_username(self, username):
        """Ввести имя пользователя"""
        logger.info(f"Entering username: {username}")
        element = self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
        element.clear()
        element.send_keys(username)
        return self
    
    def enter_password(self, password):
        """Ввести пароль"""
        logger.info("Entering password")
        element = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        element.clear()
        element.send_keys(password)
        return self
    
    def click_login(self):
        """Нажать кнопку входа"""
        logger.info("Clicking login button")
        element = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        element.click()
        return self
    
    def login(self, username, password):
        """Выполнить полный процесс входа"""
        logger.info(f"Logging in with username: {username}")
        return self.enter_username(username).enter_password(password).click_login()
    
    def get_error_message(self):
        """Получить сообщение об ошибке"""
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            message = element.text
            logger.info(f"Error message received: {message}")
            return message
        except:
            return None
    
    def is_inventory_page_loaded(self):
        """Проверить загрузку страницы инвентаря"""
        try:
            # Проверка по URL (использует неявное ожидание)
            if "inventory" in self.driver.current_url:
                logger.info("Inventory page loaded (URL check)")
                return True
            
            # Проверка по элементу (использует неявное ожидание)
            element = self.driver.find_element(*self.INVENTORY_CONTAINER)
            if element.is_displayed():
                logger.info("Inventory page loaded (element check)")
                return True
            
            return False
        except Exception as e:
            logger.warning(f"Inventory page not loaded: {e}")
            return False
    
    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url