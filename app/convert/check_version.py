import json
from logging import getLogger
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import json
from config.config_class import ConfigDefinitions
from openpyxl import Workbook

from .exceptions import DefinisionsFileException
from .class_definitions import CellInfo, DefinisionsFileInfo
from util.version_value import VersionValue

def check_workbook_version(workbook: Workbook, config: ConfigDefinitions) -> Tuple[Union[DefinisionsFileInfo, None], Union[DefinisionsFileInfo, None]]:
    applogger = getLogger('app')
    current: Union[DefinisionsFileInfo, None] = None
    latest: Union[DefinisionsFileInfo, None] = None

    for info in listup(config):
        applogger.debug(info)
        if info.version_def.sheet == '' or info.version_def.cell == '':
            continue

        if config.version != '*':
            if VersionValue(config.version) == info.version:
                current = latest = info
            if current and latest and info.compatibility == latest.compatibility and info.version > latest.version:
                latest = info
        elif info.version_def.sheet in workbook.sheetnames and info.version_def.cell:
            cell = workbook[info.version_def.sheet][info.version_def.cell]
            val = cell.value
            if val is None:
                continue
            nf = cell.number_format.split('.')
            if len(nf) == 2:
                num_format_string = f'0{nf[0].count("0")}.{nf[1].count("0")}f'
                if VersionValue(f'{val:{num_format_string}}') == info.version:
                    current = latest = info
            else:
                if VersionValue(str(val)) == info.version:
                    current = latest = info
            if current and latest and info.compatibility == latest.compatibility and info.version > latest.version:
                latest = info
    return current, latest


def check_datafile_version(datadict: Dict[str, Any], config: ConfigDefinitions) -> Tuple[Union[DefinisionsFileInfo, None], Union[DefinisionsFileInfo, None]]:
    applogger = getLogger('app')
    current: Union[DefinisionsFileInfo, None] = None
    latest: Union[DefinisionsFileInfo, None] = None

    format_version = datadict.get('format_version', None)
    for info in listup(config):
        applogger.debug(info)

        if config.version != '*':
            if VersionValue(config.version) == info.version:
                current = latest = info
            if current and latest and info.compatibility == latest.compatibility and info.version > latest.version:
                latest = info
        elif VersionValue(str(format_version)) == info.version:
            current = latest = info
        if current and latest and info.compatibility == latest.compatibility and info.version > latest.version:
            latest = info
        
    return current, latest

def listup(config: ConfigDefinitions) -> List[DefinisionsFileInfo]:
    applogger = getLogger('app')
    applogger.info(config)
    files = Path(config.folder).glob(config.file_pattern)
    latest_version = VersionValue('0.0')
    current_version = VersionValue('0.0')

    definisions_file_list: List[DefinisionsFileInfo] = []

    if not files:
        raise DefinisionsFileException('Cannot find definisions files in %s (%s)', config.folder, config.file_pattern)

    for file in files:
        with file.open('r', encoding=config.encoding) as f:
            data = json.load(f)
        current_version = VersionValue(str(data.get('format_version', '0.0')))
        if current_version > latest_version:
            latest_version = current_version
        def_cell_info = data.get('format_definition_cell')

        cell_info = CellInfo(def_cell_info.get('sheet', ''), def_cell_info.get('cell', ''))

        defs_file_info = DefinisionsFileInfo(
            name=data.get('name'),
            version=current_version,
            compatibility=VersionValue(str(data.get('format_compatibility', '0.0'))),
            filename=file,
            version_def=cell_info,
            encoding=config.encoding,
            update_date=data.get('date_updated', '')
        )

        definisions_file_list.append(defs_file_info)
    return sorted(definisions_file_list, key=lambda x: x.version)
