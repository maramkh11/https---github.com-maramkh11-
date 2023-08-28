from abc import abstractmethod
import allure
from utilities.common.assert_result import AssertResult
from utilities.common.common_enums import Menue, Page
from utilities.pages.login_page import Login
from utilities.pages.navigation_page import NavigationPage
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

    @abstractmethod
    def assert_test(self):
        pass
