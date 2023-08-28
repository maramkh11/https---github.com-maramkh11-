from datetime import datetime
import logging
import allure
import pytest

class AllureLoggingHandler(logging.handler):

    def log (self,message):
        now =datetime.now()
        current_time=now.strftime("%H:%M:%S")
        with allure.step("Log {0} : {1}".format(current_time,message)):
            pass
