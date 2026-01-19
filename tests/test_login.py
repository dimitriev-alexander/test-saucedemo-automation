import allure
import pytest
import time
from data.test_data import TestUsers, ErrorMessages

@allure.feature("Login Tests")
class TestLogin:
    
    @allure.title("Successful login with standard user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user_data", [
        TestUsers.STANDARD,
        TestUsers.PERFORMANCE
    ], ids=["standard_user", "performance_glitch_user"])
    def test_successful_logins(self, login_page, user_data):
        """Успешный логин для различных пользователей"""
        with allure.step("Open login page"):
            login_page.open()
        
        with allure.step(f"Login with {user_data['username']}"):
            login_page.login(user_data["username"], user_data["password"])
        
        with allure.step("Verify inventory page loaded"):
            assert login_page.is_inventory_page_loaded(), "Inventory page should be loaded"
            assert "inventory" in login_page.get_current_url(), "URL should contain 'inventory'"
    
    @allure.title("Login with locked out user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user(self, login_page):
        """Логин заблокированного пользователя"""
        login_page.open()
        login_page.login(TestUsers.LOCKED["username"], TestUsers.LOCKED["password"])
        
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert "locked out" in error_message.lower(), "Error should contain 'locked out'"
    
    @allure.title("Login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("credentials, expected_error", [
        (("standard_user", "wrong_password"), "do not match"),
        (("", "secret_sauce"), "username is required"),
        (("standard_user", ""), "password is required"),
        (("", ""), "username is required")
    ], ids=["wrong_password", "empty_username", "empty_password", "empty_both"])
    def test_invalid_credentials(self, login_page, credentials, expected_error):
        """Логин с невалидными данными"""
        username, password = credentials
        
        login_page.open()
        
        if username:
            login_page.enter_username(username)
        if password:
            login_page.enter_password(password)
        
        login_page.click_login()
        
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert expected_error in error_message.lower(), f"Error should contain '{expected_error}'"
    
    @allure.title("Performance test for glitch user")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_performance_glitch_timing(self, login_page):
        """Проверка времени входа для performance_glitch_user"""
        login_page.open()
        
        start_time = time.time()
        login_page.login(TestUsers.PERFORMANCE["username"], TestUsers.PERFORMANCE["password"])
        
        # Ждем загрузку с таймаутом
        timeout = 40
        while time.time() - start_time < timeout:
            if login_page.is_inventory_page_loaded():
                break
            time.sleep(1)
        
        end_time = time.time()
        login_time = end_time - start_time
        
        allure.attach(
            f"Login time: {login_time:.2f} seconds",
            name="Performance metrics",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert login_page.is_inventory_page_loaded(), "Inventory page should load within timeout"
        assert login_time < timeout, f"Login should complete in less than {timeout} seconds"