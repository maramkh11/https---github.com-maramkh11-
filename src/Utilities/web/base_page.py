import asyncio
from typing import Any, Callable, List, Optional, Tuple, TypeVar

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement

from web.web_driver_helper import WebDriverHelper

T = TypeVar('T')

ElementLocator = Tuple[str, str]

class WaitForElementTimeoutError(asyncio.exceptions.TimeoutError):
    pass

class WaitForElementExpectedStatusTimeoutError(asyncio.exceptions.TimeoutError):
    pass

class BasePage:
    def __init__(self, web_driver_helper: WebDriverHelper):
        self._web_driver_helper = web_driver_helper

    async def get_title(self) -> str:
        return await self._run_in_executor(getattr, self._web_driver, 'title')

    async def send_escape(self):
        def send_escape_async():
            actions = ActionChains(self._web_driver)
            actions.send_keys(Keys.ESCAPE)
            actions.perform()

        await self._run_in_executor(send_escape_async)

    async def find_elements(self, locator: ElementLocator) -> List[WebElement]:
        return await self._run_in_executor(self._web_driver.find_elements, *locator)

    async def wait_for_element(self, locator: ElementLocator, timeout: float = 5.0) -> WebElement:
        async def wait_for_element():
            while True:
                try:
                    return await self._run_in_executor(self._web_driver.find_element, *locator)
                except NoSuchElementException:
                    await asyncio.sleep(1.0)

        try:
            return await asyncio.wait_for(wait_for_element(), timeout)
        except asyncio.TimeoutError as exception:
            raise WaitForElementTimeoutError(
                f'wait for element timeout. {locator=}, {timeout=}') from exception

    async def wait_for_element_expected_status(
            self,
            locator: ElementLocator,
            timeout: float,
            check_expected_status: Callable[[Optional[WebElement]], bool]):

        def wait_for_element_and_check_status_async() -> bool:
            try:
                web_element = self._web_driver.find_element(*locator)
                return check_expected_status(web_element)
            except NoSuchElementException:
                return check_expected_status(None)

        async def wait_for_element_and_check_status():
            while not await self._run_in_executor(wait_for_element_and_check_status_async):
                await asyncio.sleep(1.0)

        try:
            return await asyncio.wait_for(wait_for_element_and_check_status(), timeout)
        except asyncio.TimeoutError as exception:
            raise WaitForElementExpectedStatusTimeoutError(
                f'wait for element expected status timeout. {locator=}, {timeout=}') from exception

    async def wait_for_element_and_get_is_displayed(self, locator: ElementLocator) -> bool:
        web_element = await self.wait_for_element(locator)
        return await self._run_in_executor(web_element.is_displayed)

    async def wait_for_element_and_get_is_enabled(self, locator: ElementLocator) -> bool:
        web_element = await self.wait_for_element(locator)
        return await self._run_in_executor(lambda: web_element.is_displayed() and web_element.is_enabled())

    async def wait_for_element_and_get_is_exist(self, locator: ElementLocator):
        try:
            await self.wait_for_element_is_exist(
                locator,
                1.0)
            return True
        except asyncio.exceptions.TimeoutError:
            return False

    async def wait_for_element_and_get_text(self, locator: ElementLocator) -> str:
        web_element = await self.wait_for_element(locator)
        return await self._run_in_executor(getattr, web_element, 'text')

    async def wait_for_element_and_get_attribute(
            self,
            locator: ElementLocator,
            attribute_name: str) -> str:

        web_element = await self.wait_for_element(locator)
        return await self._run_in_executor(web_element.get_attribute, attribute_name)

    async def wait_for_element_and_get_value_of_css_property(
            self,
            locator: ElementLocator,
            property_name: str) -> str:

        web_element = await self.wait_for_element(locator)
        return await self._run_in_executor(web_element.value_of_css_property, property_name)

    async def wait_for_element_is_exist(self, locator: ElementLocator, timeout: float):
        await self.wait_for_element_expected_status(
            locator,
            timeout,
            lambda web_element: web_element is not None)

    async def wait_for_element_is_not_exist(self, locator: ElementLocator, timeout: float):
        await self.wait_for_element_expected_status(
            locator,
            timeout,
            lambda web_element: web_element is None)

    async def wait_for_element_is_displayed(self, locator: ElementLocator, timeout: float):
        await self.wait_for_element_expected_status(
            locator,
            timeout,
            lambda web_element: web_element is not None and web_element.is_displayed())

    async def wait_for_element_is_not_displayed(self, locator: ElementLocator, timeout: float):
        await self.wait_for_element_expected_status(
            locator,
            timeout,
            lambda web_element: web_element is not None and not web_element.is_displayed())

    async def wait_for_element_with_text(self, locator: ElementLocator, text: str, timeout: float):
        await self.wait_for_element_expected_status(
            locator,
            timeout,
            lambda web_element: web_element is not None and web_element.text == text)

    async def wait_for_element_animated_opacity(self, locator: ElementLocator, timeout: float):
        await self.wait_for_element_expected_status(
            locator,
            timeout,
            lambda web_element: web_element is not None and web_element.value_of_css_property('opacity') == '1')

    async def wait_for_element_and_click(self, locator: ElementLocator):
        await self.wait_for_element(locator)
        await self.wait_for_element_to_be_clickable(locator)
        await self._scroll_to_element_and_click(locator)

    async def wait_for_element_and_send_keys(
            self,
            locator: ElementLocator,
            keys: str,
            clear_all: bool = False):

        web_element = await self.wait_for_element(locator)
        await self.wait_for_element_to_be_clickable(locator)
        if clear_all:
            await self._run_in_executor(web_element.send_keys, Keys.CONTROL + 'a')

        await self._run_in_executor(web_element.send_keys, keys)

    async def wait_for_element_and_send_backspace(self, locator: ElementLocator):
        await self.wait_for_element_and_send_keys(locator, Keys.BACKSPACE)

    async def wait_for_element_and_move(self, locator: ElementLocator):
        web_element = await self.wait_for_element(locator)

        def move_to_element_async():
            hover = ActionChains(self._web_driver).move_to_element(web_element)
            return hover.perform()

        return await self._run_in_executor(move_to_element_async)

    async def wait_for_element_to_be_clickable(self, locator: ElementLocator, timeout: float = 5.0) -> WebElement:
        def check_element_clickable(element: Optional[WebElement]) -> bool:
            if element is None:
                return False
            return element.is_displayed() and element.is_enabled()

        await self.wait_for_element_is_displayed(locator, timeout)
        await self.wait_for_element_expected_status(locator, timeout, check_element_clickable)
        return await self.wait_for_element(locator)

    async def wait_for_element_and_left_click_drag(
            self,
            source_locator: ElementLocator,
            target_locator: ElementLocator):

        source_element = await self.wait_for_element(source_locator)
        target_element = await self.wait_for_element(target_locator)

        def left_click_and_drag_element_async():
            actions = ActionChains(self._web_driver)
            actions.drag_and_drop(source=source_element, target=target_element)
            actions.perform()

        await self._run_in_executor(left_click_and_drag_element_async)

    async def wait_for_element_and_right_click_drag(
            self,
            source_locator: ElementLocator,
            target_locator: ElementLocator):

        source_element = await self.wait_for_element(source_locator)
        target_element = await self.wait_for_element(target_locator)

        def right_click_and_drag_element_async():
            actions = ActionChains(self._web_driver)
            actions.move_to_element(source_element)
            actions.w3c_actions.pointer_action.pointer_down(MouseButton.RIGHT)
            actions.w3c_actions.pointer_action.pointer_down(MouseButton.MIDDLE)
            actions.move_to_element(target_element)
            actions.w3c_actions.pointer_action.pointer_up(MouseButton.RIGHT)
            actions.perform()

        await self._run_in_executor(right_click_and_drag_element_async)

    async def wait_for_element_and_left_click_drag_by_offset(
            self,
            source_locator: ElementLocator,
            x_offset_value,
            y_offset_value):

        source_element = await self.wait_for_element(source_locator)

        def left_click_and_drag_element_by_offset_async():
            actions = ActionChains(self._web_driver)
            actions.click_and_hold(source_element)
            actions.move_by_offset(xoffset=x_offset_value, yoffset=y_offset_value)
            actions.release()
            actions.perform()

        await self._run_in_executor(left_click_and_drag_element_by_offset_async)

    async def _scroll_to_element_and_click(self, target_element: ElementLocator):
        element = await self.wait_for_element(target_element)

        def scroll_to_element_and_click_async():
            actions = ActionChains(self._web_driver)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()

        await self._run_in_executor(scroll_to_element_and_click_async)

    @property
    def _web_driver(self):
        return self._web_driver_helper.web_driver

    async def _run_in_executor(self, _callable: Callable[..., T], *args: Any) -> T:
        return await self._web_driver_helper.run_in_executor(_callable, *args)
