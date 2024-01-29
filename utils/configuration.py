import yaml
from utils.constants import *

class Configuration:

    def __init__(self):
        self.config = dict()

        file_content = open(CONFIGURATION_FILE_NAME, 'r')
        configuration_file = yaml.safe_load(file_content)

        self.config = configuration_file
