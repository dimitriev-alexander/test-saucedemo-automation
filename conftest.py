import pytest
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="session")
def driver():
    """Создает драйвер с настройками"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    
    # Установка неявных ожиданий (10 секунд)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)