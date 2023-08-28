import allure
from utilities.common.common_enums import Common
from utilities.common.common_functions import save_screenshot

from web.web_driver_helper import WebDriverHelper


class AllureStep:

    def __init__(self, web_driver_helper:WebDriverHelper):
        self._web_driver_helper=web_driver_helper
        self._description="Step Description"
        self._result=None
        self._is_screenshot=False

    def set_description(self,description:str,step_number:int=None):
        if step_number:
            self._description=f"{Common.STEP_NUMBER.value.format(step_number)} {description}"
        else:
             self._description=description
        return self
    
    def set_screenshot(self):
        self._is_screenshot=True
        return self    

    def set_assert_result(self,result:tuple):
        self._result=result
        return self

    def generate(self):
        self._check_result()
        with allure.step(f"{ self._description}"):
            if self._result and len(self._result)>1:
                with open(self._result[2], "rb") as file:
                    allure.attach(file.read(), name=self._result[1], attachment_type=allure.attachment_type.PNG)
            if self._is_screenshot:
                screenshot_path =save_screenshot(self._web_driver_helper,screenshot_name= self._description)
                with open(screenshot_path, "rb") as file:
                        allure.attach(file.read(), name= self._description, attachment_type=allure.attachment_type.PNG)             

    def _check_result(self):
        if self._result:
            if  self._result[0] == False:
                self._description=f"{self._description} {Common.FAILED.value}"   

















        # if self._result:
        #     if self._result[0] == False:
        #         with allure.step(f"{ self._description} {'-'*40} Failed"):
        #             with open(self._result[2], "rb") as file:
        #                 allure.attach(file.read(), name=self._result[1], attachment_type=allure.attachment_type.PNG)
        #     if self._result[0]==True:
        #         with allure.step(f"{ self._description}"):
        #             pass            
        # if self._is_screenshot:
        #     with allure.step(f"{ self._description}"):
        #         screenshot_path =save_screenshot(self._web_driver_helper,screenshot_name= self._description)
        #         with open(screenshot_path, "rb") as file:
        #                 allure.attach(file.read(), name= self._description, attachment_type=allure.attachment_type.PNG)     
        # elif not self._result and not self._is_screenshot:
        #     with allure.step(f"{ self._description}"):
        #         pass
        # return self                  