from selenium.webdriver.common.by import By
from web.base_page import BasePage
from web.web_driver_helper import WebDriverHelper


class CustomersPage(BasePage):
    # locators
    add_new_button = (By.LINK_TEXT, "Add new")
    email_input = (By.CSS_SELECTOR, "input[id='Email']")
    password_input = (By.CSS_SELECTOR, "input[id='Password']")
    save_button = (By.CSS_SELECTOR, "button[name='save']")

    def __init__(self, web_driver_helper: WebDriverHelper):
        self._web_driver_helper = web_driver_helper
        BasePage.__init__(self, web_driver_helper)
