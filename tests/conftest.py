import asyncio
import os
import shutil

import pytest

from utilities.web.web_driver_helper_singleton import WebDriverSingleton



@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
async def browser():
    browser_name = os.getenv('Browser')
    url = os.getenv("URL")
    web_driver_helper = WebDriverSingleton(browser_name, url=url)
    try:
        await web_driver_helper.maximize_window()
        await web_driver_helper.get(os.getenv('platform_url'))
        yield web_driver_helper
    finally:
        await web_driver_helper.quit()

@pytest.fixture(scope='session', autouse=True)
def remove_downloads():
    downloads_folder = os.getenv("downloads_folder")
    if not os.path.exists(downloads_folder):
        os.mkdir(downloads_folder)
    yield
    downloads_folder = os.getenv("downloads_folder")
    folder = f'./{downloads_folder}'
    if os.path.exists(folder) and downloads_folder != '':
        files = os.listdir(folder)
        if len(files) > 0:
            shutil.rmtree(folder)
