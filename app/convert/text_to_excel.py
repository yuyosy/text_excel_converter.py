from logging import getLogger
from pathlib import Path
from typing import Any, Callable, Dict

from config.config_class import ConfigApp
from openpyxl.workbook.workbook import Workbook

from .check_version import check_datafile_version
from .class_definitions import Definitions
from .converter import Converter
from .load_definitions import load_definisions
from .set_metadata import set_metadata
from .write_keyvalue import write_keyvalue
from .write_table import write_table

applogger = getLogger('app')
filelogger = getLogger('file')



from .converter import Converter


class TextToExcel(Converter):
    def __init__(self, config: ConfigApp) -> None:
        super().__init__(config)
        
        self.read_action: Dict[str, Callable] = {
            'key-value': write_keyvalue,
            'table': write_table
        }


    def read(self, datadict:Dict[str, Any], *, filename:Path) -> None:
        applogger.info('@read')
        self.data.update(datadict)
        current, latest = check_datafile_version(datadict.get('$metadata', {}), self.config.options.definitions)
        applogger.info('@checked workbook version')
        applogger.info('CurrentVersion: %s', current)
        applogger.info('LatestVersion: %s', latest)
        if not current:
            raise Exception
        self.definition_data = load_definisions(current)
        filelogger.debug(self.definition_data)


    def write(self, path:Path) -> None:
        applogger.info('@write')
