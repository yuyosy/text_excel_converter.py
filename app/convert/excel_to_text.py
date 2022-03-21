import json
from logging import getLogger
from pathlib import Path
from typing import Any, Callable, Dict

from config.config_class import ConfigApp
from openpyxl.workbook.workbook import Workbook

from .check_version import check_workbook_version
from .converter import Converter
from .definitions_class import Definitions
from .load_definitions import load_definisions
from .read_keyvalue import read_keyvalue
from .read_table import read_table

applogger = getLogger('app')


class ExcelToText(Converter):
    def __init__(self, config: ConfigApp) -> None:
        super().__init__(config)
        
        self.read_action: Dict[str, Callable] = {
            'key-value': read_keyvalue,
            'table': read_table
        }

    def read(self, workbook: Workbook) -> None:
        applogger.info('@read')
        current, latest = check_workbook_version(workbook, self.config.options.definitions)
        applogger.info('@checked workbook version')
        applogger.info('CurrentVersion: %s', current)
        applogger.info('LatestVersion: %s', latest)
        if not current:
            raise Exception
        self.definition_data = load_definisions(current)
        applogger.debug(self.definition_data)

        for name in self.definition_data.includes:
            applogger.info(f'Processing: {name}')
            definitions = self.definition_data.definitions.get(name, None)
            if not definitions or not self.read_action.get(definitions.type) or workbook[definitions.sheet] is None:
                continue
            read_action: Callable[[Workbook, Definitions], Dict[str, Any]] = self.read_action.get(definitions.type, lambda: print('Unknown function'))
            for k, v in read_action(workbook, definitions):
                self.data.set(k, v)

    def write(self, path: Path) -> None:
        applogger.info('@write')
    
        with path.open('w', encoding='utf-8') as f:
            f.write(json.dumps(self.data.asattrdict(), indent=4, ensure_ascii=False, default=str))
