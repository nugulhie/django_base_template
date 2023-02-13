import logging
import sys
import traceback

import typing_extensions

LoggingCategoryValue = typing_extensions.Literal[
    "BASE"
]


class Logging:
    def __init__(self, category: LoggingCategoryValue):
        self.category = category
        self.logger = logging.getLogger("django.server")

    def get_log_string(self, message, e: Exception):
        func_name = self.who_am_i()
        return f"[{self.category}][{func_name}] : {message} : {e}"

    def exception(self, message, e: Exception):
        self.logger.exception(self.get_log_string(message, e))

    def error(self, message, e: Exception):
        self.logger.error(self.get_log_string(message, e))

    def info(self, message):
        self.logger.info(message)

    def debug(self, message, e: Exception):
        self.logger.debug(self.get_log_string(message, e))

    def log(self, level, message, e: Exception):
        if level == "DEBUG":
            self.debug(message, e)
        if level == "INFO":
            self.info(message)
        if level == "ERROR":
            self.error(message, e)
        if level == "CRITICAL":
            self.exception(message, e)

    def who_am_i(self):
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)
        fname = stk[0][2]
        # stack = traceback.extract_stack()
        # filename, codeline, funcName, text = stack[-4]

        return fname