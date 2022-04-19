from enum import Flag, auto
from pathlib import Path


class FileType(Flag):
    JSON = auto()
    Excel = auto()


class InputFileInfo():
    def __init__(self, file: Path) -> None:
        self.file = file
        if file.suffix in ['.json']:
            self.file_type = FileType.JSON
        elif file.suffix in ['.xlsx']:
            self.file_type = FileType.Excel
        
        self.convert_to = {
            FileType.JSON: '.xlsx',
            FileType.Excel: '.json'
        }

    @property
    def convert_to_ext(self) -> str:
        return self.convert_to.get(self.file_type, '')
