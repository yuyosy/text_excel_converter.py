class ConvertException(Exception):
    pass

class DefinisionsFileException(ConvertException):
    pass

class ExcelToTextException(ConvertException):
    pass

class TextToExcelException(ConvertException):
    pass

class DataOutputException(ConvertException):
    pass