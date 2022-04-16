class ConverterBaseException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg


# DefinisionsFile
class DefinisionsFileException(ConverterBaseException):
    pass


# Data Convert
class DataConvertException(ConverterBaseException):
    pass


class ExcelToTextException(DataConvertException):
    pass


class TextToExcelException(DataConvertException):
    pass


# Data IO
class DataIOException(ConverterBaseException):
    pass


class DataInputException(DataIOException):
    pass


class DataOutputException(DataIOException):
    pass
