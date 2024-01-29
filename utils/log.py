from utils.constants import *
from datetime import datetime
import os


class Log:

    def __init__(self):
        self.file_log = open(LOG_FILE_NAME, "a")
        actual_size_log_file = os.stat(LOG_FILE_NAME).st_size / (1024*1024)
        if LOG_MAX_SIZE_MEGA_BYTES < actual_size_log_file:
            self.file_log.close()
            os.rename(LOG_FILE_NAME, LOG_FILE_NAME+"."+datetime.now().strftime("%Y%m%d%H%M%S"))
            self.file_log = open(LOG_FILE_NAME, "a")

    def log(self, subject:str, message:str):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_line = date_now + " ["+subject+"] " + message
        self.file_log.write(new_line + "\n")
        self.file_log.flush()
        print(new_line)

    def close(self):
        self.file_log.close()
