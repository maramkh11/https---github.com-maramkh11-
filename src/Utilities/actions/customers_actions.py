import allure
from utilities.actions.base_actions import BaseActions
from utilities.common.allure_step import AllureStep
from utilities.common.assert_result import AssertResult
from utilities.pages.customers_page import CustomersPage
from web.web_driver_helper import WebDriverHelper


class CustomersActions(BaseActions):
    
    def __init__(self, web_driver_helpere:WebDriverHelper):
        self._web_driver_helper =web_driver_helpere
        self._customers_page = CustomersPage(web_driver_helpere)
        self._assert_result=AssertResult(web_driver_helpere)
        self._allure_step=AllureStep(web_driver_helpere)
        BaseActions.__init__(self,web_driver_helpere)

    def assert_test(self):
        self._assert_result.assert_all()
    
    async def click_on_add_new_button(self,step_number):
        await self._customers_page.wait_for_element_and_click(self._customers_page.add_new_button)
        self._allure_step.set_description("Click on Add new new button",step_number).generate()

    async def insert_email(self, step_number,value):
        await self._customers_page.wait_for_element_and_send_keys(self._customers_page.email_input, value)
        input_value = await self._customers_page.wait_for_element_and_get_text(self._customers_page.email_input)
        result=self._assert_result.is_equal(input_value, value, f"expected {value} but {input_value}")
        self._allure_step.set_description(f"Insert Email = {value} and validate",step_number).set_assert_result(result).generate()
