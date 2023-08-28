import asyncio
import functools
import os
from typing import Any, Callable, Optional, TypeVar

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


T = TypeVar('T')

class WebDriverSingleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WebDriverSingleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self,browser_name:str,url=None):
        if not hasattr(self, '_web_driver'):
            if url:
                web_driver_url =url 
                remote_driver = functools.partial(webdriver.Remote, command_executor=web_driver_url)
                options=self.add_driver_properties(is_dockerized=True)
                self._web_driver = remote_driver(options=options)
            else:
                service = ChromeService(executable_path=ChromeDriverManager().install())
                options=self.add_driver_properties()
                self._web_driver  = webdriver.Chrome(service=service,options=options)              
        self._keep_alive_task: Optional[asyncio.Future] = None
 

    @property
    def web_driver(self):
        return self._web_driver

    async def get(self, url: str):
        await self.run_in_executor(self._web_driver.get, url)

    async def back(self):
        await self.run_in_executor(self._web_driver.back)

    async def current_url(self):
        await asyncio.sleep(2)
        return self._web_driver.current_url

    async def quit(self):
        def quit_async():
            self.web_driver.close()
            self.web_driver.quit()

        await self.run_in_executor(quit_async)

    async def close(self):
        def close_async():
            self.web_driver.close()

        await self.run_in_executor(close_async)    

    def save_screenshot(self,screenshot):
        return self._web_driver.save_screenshot(screenshot)
    
    async def maximize_window(self):
        await self.run_in_executor(self.web_driver.maximize_window)

    def start_keep_alive(self):
        async def keep_alive_async():
            while True:
                await asyncio.sleep(60.0)
                await self.run_in_executor(self.web_driver.execute, 'getCurrentUrl')

        self._keep_alive_task = asyncio.create_task(keep_alive_async())

    def stop_keep_alive(self):
        if self._keep_alive_task is None:
            raise ValueError('self._keep_alive_task is None')

        self._keep_alive_task.cancel()

    async def run_in_executor(self, _callable: Callable[..., T], *args: Any) -> T:
        return await asyncio.get_running_loop().run_in_executor(None,_callable,*args)

    def add_driver_properties(self,is_dockerized=False) -> Options:
        options = Options()
        if not is_dockerized:
            downloads_dir=os.path.abspath(f'./{os.getenv("DOWNLOADS_FOLDER")}')
        else:
            downloads_dir="/home/seluser/Downloads"

        preferences = {'download.default_directory': downloads_dir,
                       "download.prompt_for_download": False,
                       "download.directory_upgrade": True,
                       "safebrowsing.enabled": True}
        options.add_experimental_option('prefs', preferences)
        return options
    