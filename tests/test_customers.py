import pytest
from Utilities.actions.customers_actions import CustomersActions
from Utilities.common.common_enums import Menue, Page
from Utilities.pages.customers_page import CustomersPage

pytestmark = pytest.mark.asyncio

class TestCustomers:

    async def test_add_new_customer(self,browser):
        driver = browser
        customers_page=CustomersPage(driver)
        actions=CustomersActions(customers_page)
        await actions.login()
        await actions.get_page(Menue.CUSTOMERS,Page.CUSTOMERS)
        await actions.click_on_add_new_button()
        await actions.insert_email("automation@automation.com")
