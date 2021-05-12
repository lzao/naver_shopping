import constant
import os
from datetime import *


class Error(object):

    # noinspection PyMethodMayBeStatic
    def logging(self, error_message=''):
        current_datetime = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
        today = "{:%Y%m%d}".format(date.today())
        error_log_file_name = "%s/logs/error_log_%s.txt" % (constant.ROOT_PATH, today)
        if os.path.isfile(error_log_file_name):
            f = open(error_log_file_name, "a")
        else:
            f = open(error_log_file_name, "w", encoding="UTF8")
        error_stack = "[" + current_datetime + "]" + ": " + error_message + "\n"
        f.write(error_stack)
        f.close()
