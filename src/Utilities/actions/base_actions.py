import allure
from Utilities.common.common_enums import Menue, Page
from Utilities.pages.login_page import Login
from Utilities.pages.navigation_page import NavigationPage
from web.web_driver_helper import WebDriverHelper


class BaseActions:

    def __init__(self, web_driver_helper: WebDriverHelper):
        self._web_driver_helper = web_driver_helper

    @allure.step("Login")
    async def login(self):
        await Login(self._web_driver_helper).login()

    @allure.step("Get Page")
    async def get_page(self, menue: Menue, page: Page):
        await NavigationPage(self._web_driver_helper).get_page(menue.value, page.value)
