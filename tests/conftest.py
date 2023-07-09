
import asyncio
import os

import pytest
from web.web_driver_helper import WebDriverHelper



@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def browser():
    browser_name = os.getenv('Browser')
    url = os.getenv("URL")
    web_driver_helper = WebDriverHelper(browser_name,url=url)
    try:
        await web_driver_helper.maximize_window()
        await web_driver_helper.get(os.getenv('platform_url'))
        yield web_driver_helper
    finally:
        await web_driver_helper.quit()
   
        
@pytest.fixture(scope='session', autouse=True)
def remove_downloads():
    pass