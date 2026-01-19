"""
Test data for login tests
"""

class TestUsers:
    STANDARD = {
        "username": "standard_user",
        "password": "secret_sauce",
        "expected": "success"
    }
    
    LOCKED = {
        "username": "locked_out_user",
        "password": "secret_sauce",
        "expected": "locked_error"
    }
    
    PERFORMANCE = {
        "username": "performance_glitch_user",
        "password": "secret_sauce",
        "expected": "success"
    }
    
    PROBLEM = {
        "username": "problem_user",
        "password": "secret_sauce",
        "expected": "success"
    }


class ErrorMessages:
    INVALID_CREDENTIALS = "Epic sadface: Username and password do not match"
    LOCKED_USER = "Epic sadface: Sorry, this user has been locked out."
    REQUIRED_USERNAME = "Epic sadface: Username is required"
    REQUIRED_PASSWORD = "Epic sadface: Password is required"
    REQUIRED_BOTH = "Epic sadface: Username is required"