import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logging import getLogger
import sys

from openpyxl import load_workbook

from applogging.logger import default_logger_config, set_logger_config
from config.config import init_config
from convert.excel_to_text import ExcelToText
from convert.exceptions import DefinisionsFileException
from util.resource_path import resource_path


def set_parser() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--config', metavar='<Config Path>', default=resource_path('config.yaml'))
    parser.add_argument('-i', '--input', metavar='<Input Path>')
    parser.add_argument('-o', '--output', metavar='<Output Path>')
    parser.add_argument('-m', '--mode', metavar='<Preset Mode>', default='default')
    return parser


if __name__ == '__main__':
    exit_code = 0
    default_logger_config()
    applogger = getLogger('app')

    parser = set_parser()
    args = parser.parse_args()

    try:
        config = init_config(args.config, 'utf-8')
        set_logger_config(config.logging)
        # file = input('Input>>') if args.input is None else args.input
        file = resource_path('data/input/1.0.xlsx') # -------------DEBUG

        workbook = load_workbook(file.as_posix(), read_only=True, data_only=True)
        appconfig = config.presets.get(args.mode)
        if not appconfig:
            raise Exception            
        converter = ExcelToText(appconfig)
        converter.read(workbook, filename=file)
        converter.write(resource_path('data/output/1.0.json'))
    except DefinisionsFileException as err:
        applogger.exception(err)
        exit_code = 21
    except Exception as err:
        applogger.exception(err)
        exit_code = 1
    applogger.info('Finished')
    sys.exit(exit_code)