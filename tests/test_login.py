# tests/test_login.py
import allure
import pytest
import time

@allure.feature("Login Tests")
class TestLogin:
    
    @allure.title("Test 1: Successful login with standard user")
    def test_successful_login(self, login_page):
        """Успешный логин"""
        print("\n" + "="*50)
        print("ТЕСТ 1: Успешный логин")
        print("="*50)
        
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        
        # Ждем инвентарь
        assert login_page.wait_for_inventory(timeout=15)
        assert "inventory" in login_page.get_current_url()
        print("✓ Тест 1 пройден")
    
    @allure.title("Test 2: Login with invalid password")
    def test_invalid_password(self, login_page):
        """Логин с неверным паролем"""
        print("\n" + "="*50)
        print("ТЕСТ 2: Неверный пароль")
        print("="*50)
        
        login_page.open()
        login_page.login("standard_user", "wrong_password")
        
        # Ждем сообщение об ошибке
        time.sleep(2)
        error = login_page.get_error_message()
        assert error is not None
        assert "do not match" in error
        print("✓ Тест 2 пройден")
    
    @allure.title("Test 3: Login with locked out user")
    def test_locked_out_user(self, login_page):
        """Логин заблокированного пользователя"""
        print("\n" + "="*50)
        print("ТЕСТ 3: Заблокированный пользователь")
        print("="*50)
        
        login_page.open()
        login_page.login("locked_out_user", "secret_sauce")
        
        # Ждем сообщение об ошибке
        time.sleep(2)
        error = login_page.get_error_message()
        assert error is not None
        assert "locked out" in error.lower()
        print("✓ Тест 3 пройден")
    
    @allure.title("Test 4: Login with empty fields")
    def test_empty_fields(self, login_page):
        """Логин с пустыми полями"""
        print("\n" + "="*50)
        print("ТЕСТ 4: Пустые поля")
        print("="*50)
        
        login_page.open()
        login_page.click_login()
        
        # Ждем сообщение об ошибке
        time.sleep(2)
        error = login_page.get_error_message()
        assert error is not None
        assert "required" in error.lower()
        print("✓ Тест 4 пройден")
    
    @allure.title("Test 5: Login with performance glitch user")
    def test_performance_glitch_user(self, login_page):
        """Логин пользователем performance_glitch_user"""
        print("\n" + "="*50)
        print("ТЕСТ 5: Performance glitch user")
        print("="*50)
        
        login_page.open()
        
        start_time = time.time()
        login_page.login("performance_glitch_user", "secret_sauce")
        
        # Ждем дольше для этого пользователя
        inventory_loaded = login_page.wait_for_inventory(timeout=40)
        end_time = time.time()
        
        login_time = end_time - start_time
        print(f"Время входа: {login_time:.2f} секунд")
        
        assert inventory_loaded, "Инвентарь не загрузился"
        assert "inventory" in login_page.get_current_url()
        print("✓ Тест 5 пройден")