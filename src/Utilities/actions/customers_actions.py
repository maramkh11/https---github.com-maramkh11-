import allure
from Utilities.actions.base_actions import BaseActions
from Utilities.common.assert_result import AssertResult
from Utilities.common.common_enums import Status
from Utilities.pages.customers_page import CustomersPage


class CustomersActions(BaseActions):

    def __init__(self, customers_page: CustomersPage):
        self.customers_page = customers_page
        self._web_driver_helper = customers_page._web_driver_helper
        BaseActions.__init__(self, customers_page._web_driver_helper)

    @allure.step("Click on Add new new button")
    async def click_on_add_new_button(self):
        await self.customers_page.wait_for_element_and_click(self.customers_page.add_new_button)

    @allure.step("Insert Email and validate")
    async def insert_email(self, value):
        await self.customers_page.wait_for_element_and_send_keys(self.customers_page.email_input, value)
        input_value = await self.customers_page.wait_for_element_and_get_text(self.customers_page.email_input)
        AssertResult(input_value, value, Status.EQUAL, f"expected {value} but {input_value}")
