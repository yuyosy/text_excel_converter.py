class ConfigBaseException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg

# Config
class ConfigFileException(ConfigBaseException):
    pass