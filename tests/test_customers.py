import pytest
from utilities.actions.customers_actions import CustomersActions
from utilities.common.common_enums import Menue, Page

pytestmark = pytest.mark.asyncio

class TestCustomers:

    async def test_add_new_customer(self,browser):
        driver = browser
        actions=CustomersActions(driver)
        await actions.login()
        await actions.get_page(Menue.CUSTOMERS,Page.CUSTOMERS)
        await actions.click_on_add_new_button(1)
        await actions.insert_email(2,"automation@automation.com")
        await actions.assert_test()
