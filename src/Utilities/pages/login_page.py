from selenium.webdriver.common.by import By
from web.base_page import BasePage
from web.web_driver_helper import WebDriverHelper


class Login(BasePage):
    user_name_input = (By.CSS_SELECTOR, "input[id='Email']")
    password_input = (By.CSS_SELECTOR, "input[id='Password']")
    login_button = (By.XPATH, "//button[text()='Log in']")

    def __init__(self, web_driver_helper: WebDriverHelper):
        self._web_driver_helper = web_driver_helper
        BasePage.__init__(self, web_driver_helper)

    async def login(self):
        # await self.send_escape()
        # await self.wait_for_element_and_send_keys(self.user_name_input,os.getenv("username"))
        # await self.wait_for_element_and_send_keys(self.password_input,os.getenv("password"))
        await self.wait_for_element_and_click(self.login_button)
