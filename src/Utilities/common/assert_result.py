from utilities.common.common_functions import save_screenshot
from web.web_driver_helper import WebDriverHelper


class AssertResult:
    test_flag=True

    def __init__(self, web_driver_helper: WebDriverHelper):
        self._web_driver_helper= web_driver_helper

    def assert_all(self):
        if self.test_flag:
            assert True, "Test Passed"
        else:
            self.test_flag=True
            assert False, "Test Failed"      

    def _check_condition(self, condition: str, actual_result, expected_result, error_message: str):
        if not eval(condition):
            result = (False, error_message,save_screenshot(self._web_driver_helper,screenshot_name=error_message))
            self.test_flag=False
        return result

    def is_equal(self, actual_result, expected_result, error_message: str):
        return self._check_condition("actual_result == expected_result", actual_result, expected_result, error_message)

    def is_not_equal(self, actual_result, expected_result, error_message: str):
        return self._check_condition("actual_result != expected_result", actual_result, expected_result, error_message)

    def is_contain(self, actual_result, expected_result, error_message: str):
        return self._check_condition("actual_result in expected_result", actual_result, expected_result, error_message)       
