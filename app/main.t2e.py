import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logging import getLogger
import sys

from openpyxl import load_workbook

from applogging.logger import default_logger_config, set_logger_config
from config.config import init_config
from convert.text_to_excel import TextToExcel
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
