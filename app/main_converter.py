import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logging import getLogger

from openpyxl import load_workbook

from applogging.logger import default_logger_config, set_logger_config
from base.build_datetime import BUILD_DATE, BUILD_TIME
from base.input_fileinfo import FileType, InputFileInfo
from config.config import init_config
from config.exceptions import ConfigBaseException, ConfigFileException
from convert.converter import Converter
from convert.excel_to_text import ExcelToText
from convert.exceptions import (ConverterBaseException, DataConvertException,
                                DataInputException, DataIOException)
from convert.load_datafile import load_textfile
from convert.text_to_excel import TextToExcel
from convert.util_filename import (placeholder_to_savename,
                                   set_savename_datetime,
                                   setup_filename_placeholder,
                                   sourcepath_to_placeholder)
from util.resource_path import resource_path


def set_parser() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--config', metavar='<Config Path>', default=resource_path('config.yaml'))
    parser.add_argument('-i', '--input', metavar='<Input Path>')
    parser.add_argument('-o', '--output', metavar='<Output Path>')
    parser.add_argument('-m', '--mode', metavar='<Preset Mode>', default='default')
    parser.add_argument('-ndt', '--no-datetime', action='store_false')
    return parser


def make_savename(converter: Converter, file_info: InputFileInfo, include_datetime: bool = True) -> str:
    tmpl_placeholder = setup_filename_placeholder(converter.definition_data, converter.data)
    src_placeholder = sourcepath_to_placeholder(file_info.file)
    save_name = placeholder_to_savename(tmpl_placeholder, src_placeholder, include_datetime)
    save_name = set_savename_datetime(save_name, converter.metadata)
    return save_name+file_info.convert_to_ext


if __name__ == '__main__':
    version = 'dev0.1'
    exit_code = 0

    appinfo = f'Text-Excel Converter [ver.{version}]'
    builfinfo = f'Build: {BUILD_DATE}, {BUILD_TIME}'
    print(appinfo)
    print(builfinfo)

    default_logger_config()
    applogger = getLogger('app')
    filelogger = getLogger('file')
    filelogger.info(appinfo)
    filelogger.info(builfinfo)

    parser = set_parser()
    args = parser.parse_args()

    try:
        config = init_config(args.config, 'utf-8')
        set_logger_config(config.logging)
        appconfig = config.presets.get(args.mode)
        if not appconfig:
            raise ConfigFileException(99, f'No matching preset found: {args.mode}')

        file = resource_path(input('Input>>') if args.input is None else args.input)
        if not file.exists():
            raise DataInputException(9, f'Input file not found: {file.as_posix()}')

        file_info = InputFileInfo(file)

        if file_info.file_type == FileType.JSON:
            datadict = load_textfile(file)
            converter = TextToExcel(appconfig)
            converter.read(datadict, filename=file)
            output = file.with_name(make_savename(converter, file_info, args.no_datetime)) if args.output is None else resource_path(args.output)
            converter.write(output)
        elif file_info.file_type == FileType.Excel:
            workbook = load_workbook(file.as_posix(), read_only=True, data_only=True)
            converter = ExcelToText(appconfig)
            converter.read(workbook, filename=file)
            output = file.with_name(make_savename(converter, file_info, args.no_datetime)) if args.output is None else resource_path(args.output)
            converter.write(output)
    except (ConfigFileException, DataConvertException, DataIOException) as err:
        applogger.error(err)
        exit_code = err.code
    except (ConfigBaseException, ConverterBaseException) as err:
        applogger.exception(err)
        exit_code = err.code
    except KeyboardInterrupt:
        applogger.info('keyboard Interrupt! (Ctrl+C)')
        exit_code = 2
    except Exception as err:
        applogger.exception(err)
        exit_code = 1
    applogger.info(f'Finished{"!" if exit_code == 0 else " in failure."}')
    sys.exit(exit_code)
