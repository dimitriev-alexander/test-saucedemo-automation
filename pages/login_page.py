# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Увеличиваем до 15 секунд
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    
    def open(self):
        """Открыть страницу с повторными попытками"""
        print("Открываем страницу логина...")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                self.driver.get("https://www.saucedemo.com/")
                
                # Ждем появления поля ввода имени пользователя
                self.wait.until(
                    EC.presence_of_element_located(self.USERNAME_INPUT)
                )
                print(f"✓ Страница успешно загружена (попытка {attempt + 1})")
                return self
                
            except Exception as e:
                print(f"✗ Ошибка при загрузке (попытка {attempt + 1}): {str(e)[:100]}...")
                if attempt < max_attempts - 1:
                    print("Повторная попытка...")
                    time.sleep(2)
                else:
                    print("Все попытки исчерпаны")
                    # Возможно страница все же частично загрузилась, продолжаем
                    return self
    
    def enter_username(self, username):
        """Ввести имя пользователя"""
        print(f"Вводим имя пользователя: {username}")
        
        element = self.wait.until(
            EC.element_to_be_clickable(self.USERNAME_INPUT)
        )
        element.clear()
        element.send_keys(username)
        
        return self
    
    def enter_password(self, password):
        """Ввести пароль"""
        print("Вводим пароль")
        
        element = self.wait.until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        element.clear()
        element.send_keys(password)
        
        return self
    
    def click_login(self):
        """Нажать кнопку входа"""
        print("Нажимаем кнопку входа")
        
        element = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        element.click()
        
        # Даем время на обработку
        time.sleep(1)
        
        return self
    
    def login(self, username, password):
        """Выполнить вход в систему"""
        print(f"Выполняем вход для пользователя: {username}")
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        
        return self
    
    def get_error_message(self):
        """Получить сообщение об ошибке"""
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            message = element.text
            print(f"Получено сообщение об ошибке: {message}")
            return message
        except:
            return None
    
    def is_inventory_page_displayed(self, timeout=20):
        """Проверить, отображается ли страница инвентаря"""
        print("Проверяем загрузку инвентаря...")
        
        try:
            # Сначала проверяем по URL
            for _ in range(timeout):
                current_url = self.driver.current_url
                if "inventory" in current_url:
                    print(f"✓ Инвентарь найден по URL: {current_url}")
                    return True
                time.sleep(1)
            
            # Затем проверяем по элементу
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.INVENTORY_CONTAINER)
            )
            print("✓ Инвентарь найден по элементу")
            return element.is_displayed()
            
        except:
            print("✗ Инвентарь не найден")
            return False
    
    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url
    
    def wait_for_inventory(self, timeout=30):
        """Ждать загрузки инвентаря"""
        print(f"Ждем загрузку инвентаря (таймаут: {timeout}с)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Проверяем URL
                if "inventory" in self.driver.current_url:
                    print("✓ Инвентарь загружен (по URL)")
                    return True
                
                # Проверяем элемент
                element = self.driver.find_element(*self.INVENTORY_CONTAINER)
                if element.is_displayed():
                    print("✓ Инвентарь загружен (по элементу)")
                    return True
                    
            except:
                pass
            
            time.sleep(1)
        
        print(f"✗ Таймаут ожидания инвентаря ({timeout}с)")
        return False