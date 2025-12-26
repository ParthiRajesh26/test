# reg.py: Production-ready Selenium test automation for User Registration feature

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserRegistrationTests(unittest.TestCase):
    REGISTRATION_URL = "https://example.com/register"  # Replace with actual URL
    WELCOME_URL = "https://example.com/welcome"  # Replace with actual URL

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.REGISTRATION_URL)
        self.wait = WebDriverWait(self.driver, 10)
        logging.info("Browser launched and navigated to registration page.")

    def tearDown(self):
        self.driver.quit()
        logging.info("Browser closed.")

    def fill_registration_form(self, name, email, password):
        driver = self.driver
        try:
            name_input = self.wait.until(EC.presence_of_element_located((By.NAME, "name")))
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))

            name_input.clear()
            name_input.send_keys(name)
            email_input.clear()
            email_input.send_keys(email)
            password_input.clear()
            password_input.send_keys(password)
            logging.info(f"Filled registration form with Name: {name}, Email: {email}, Password: {'*'*len(password)}")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Form field not found: {e}")
            self.fail("Registration form field missing.")

    def click_register(self):
        driver = self.driver
        try:
            register_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']")))
            register_btn.click()
            logging.info("Clicked the 'Register' button.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Register button not found/clickable: {e}")
            self.fail("Register button missing or not clickable.")

    def test_successful_registration(self):
        """Scenario: Successful registration with valid details"""
        valid_name = "Test User"
        valid_email = "test.user@example.com"
        valid_password = "StrongPass123!"
        self.fill_registration_form(valid_name, valid_email, valid_password)
        self.click_register()
        try:
            # Check account creation by presence of success message or redirect
            self.wait.until(EC.url_to_be(self.WELCOME_URL))
            logging.info("Redirected to welcome page after successful registration.")
            self.assertEqual(self.driver.current_url, self.WELCOME_URL)
        except TimeoutException:
            logging.error("Did not redirect to welcome page after registration.")
            self.fail("User was not redirected to welcome page after registration.")

    def test_registration_invalid_email(self):
        """Scenario: Registration with invalid email format"""
        name = "Test User"
        invalid_email = "invalid-email"
        password = "StrongPass123!"
        self.fill_registration_form(name, invalid_email, password)
        self.click_register()
        try:
            error_msg = self.wait.until(EC.visibility_of_element_located((By.ID, "email-error")))
            self.assertIn("invalid email", error_msg.text.lower())
            logging.info("Error message for invalid email displayed as expected.")
        except TimeoutException:
            logging.error("No error message for invalid email format.")
            self.fail("Error message for invalid email not displayed.")
        # Ensure account not created by checking URL did not change
        self.assertNotEqual(self.driver.current_url, self.WELCOME_URL)

    def test_registration_weak_password(self):
        """Scenario: Registration with weak password"""
        name = "Test User"
        email = "test.user@example.com"
        weak_password = "123"
        self.fill_registration_form(name, email, weak_password)
        self.click_register()
        try:
            error_msg = self.wait.until(EC.visibility_of_element_located((By.ID, "password-error")))
            self.assertIn("too weak", error_msg.text.lower())
            logging.info("Error message for weak password displayed as expected.")
        except TimeoutException:
            logging.error("No error message for weak password.")
            self.fail("Error message for weak password not displayed.")
        # Ensure account not created by checking URL did not change
        self.assertNotEqual(self.driver.current_url, self.WELCOME_URL)

if __name__ == "__main__":
    unittest.main()
