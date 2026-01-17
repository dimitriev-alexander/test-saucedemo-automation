# conftest.py
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    """Создает драйвер с минимальными настройками"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Увеличиваем таймаут загрузки страницы
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=options)
    
    # Увеличиваем все таймауты
    driver.implicitly_wait(10)  # 10 секунд на поиск элементов
    driver.set_page_load_timeout(30)  # 30 секунд на загрузку страницы
    driver.set_script_timeout(30)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs.get('driver')
            if driver:
                screenshot = driver.get_screenshot_as_base64()
                allure.attach(
                    screenshot,
                    name=f"screenshot_on_failure_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except:
            pass