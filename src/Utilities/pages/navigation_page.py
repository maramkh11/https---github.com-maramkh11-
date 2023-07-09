from selenium.webdriver.common.by import By
from web.base_page import BasePage

from web.web_driver_helper import WebDriverHelper


class NavigationPage(BasePage):
    menue_locator = "//a[@href='#']//p[contains(text(),'{}')]/.."
    page_locator = "//li//p[text()=' {}']"

    def __init__(self, web_driver_helper: WebDriverHelper):
        self._web_driver_helper = web_driver_helper
        BasePage.__init__(self, web_driver_helper)

    async def get_page(self, menue, page):
        menue_element = (By.XPATH, self.menue_locator.format(menue))
        page_element = (By.XPATH, self.page_locator.format(page))
        await self.wait_for_element_and_click(menue_element)
        await self.wait_for_element_and_click(page_element)
