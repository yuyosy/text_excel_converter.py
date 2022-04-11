class ConvertException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg

class DefinisionsFileException(ConvertException):
    pass

class ExcelToTextException(ConvertException):
    pass

class TextToExcelException(ConvertException):
    pass

class DataOutputException(ConvertException):
    pass