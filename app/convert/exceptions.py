class ConverterBaseException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg


class DefinisionsFileException(ConverterBaseException):
    pass


class DataConvertException(ConverterBaseException):
    pass


class ExcelToTextException(DataConvertException):
    pass


class TextToExcelException(DataConvertException):
    pass


class DataIOException(ConverterBaseException):
    pass


class DataInputException(DataIOException):
    pass


class DataOutputException(DataIOException):
    pass
