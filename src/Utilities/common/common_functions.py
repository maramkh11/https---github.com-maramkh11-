import os
from web.web_driver_helper import WebDriverHelper


def save_screenshot(web_driver_helper:WebDriverHelper,screenshot_name):
    downloads_folder = os.getenv('downloads_folder')
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    screenshot_path=  "./"+downloads_folder+"/"+screenshot_name+'.png'
    web_driver_helper.save_screenshot(screenshot_path)
    return screenshot_path


def attach_screenshot():
    pass
