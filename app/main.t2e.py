import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logging import getLogger
from pathlib import Path

from applogging.logger import default_logger_config, set_logger_config
from config.config import init_config
from config.exceptions import ConfigException
from convert.exceptions import ConvertException
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


def make_savename(converter: TextToExcel, sourcefile: Path) -> str:
    tmpl_placeholder = setup_filename_placeholder(converter.definition_data, converter.data)
    src_placeholder = sourcepath_to_placeholder(sourcefile)
    save_name = placeholder_to_savename(tmpl_placeholder, src_placeholder)
    save_name = set_savename_datetime(save_name, converter.metadata)
    return save_name+'.xlsx'


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
        file = resource_path('data/input/1.0.json')  # -------------DEBUG

        appconfig = config.presets.get(args.mode)
        if not appconfig:
            raise Exception

        datadict = load_textfile(file)

        converter = TextToExcel(appconfig)
        converter.read(datadict, filename=file)
        converter.write(resource_path('data/output/output-1.0.xlsx'))

    except ConvertException as err:
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
