from pathlib import Path

from dacite.core import from_dict
from ruamel.yaml import YAML

from .config_class import Config
from .const import config_string
from .exceptions import ConfigBaseException, ConfigFileException


def init_config(config_path: Path, encoding: str = 'utf-8') -> Config:
    try:
        create_config(config_path, encoding)  # ------------- DEBUG
        if not config_path.exists():
            create_config(config_path, encoding)
        return load_config(config_path, encoding)
    except ConfigBaseException as err:
        raise err
    except Exception as err:
        raise ConfigBaseException(99, str(err)) from err


def load_config(config_path: Path, encoding: str = 'utf-8') -> Config:
    try:
        yaml = YAML(typ="safe")
        with config_path.open('r', encoding=encoding) as f:
            config_data = yaml.load(f)
        return from_dict(data_class=Config, data=config_data)
    except FileNotFoundError as err:
        raise ConfigFileException(99, f'Config file not found: {config_path}')
    except PermissionError as err:
        raise ConfigFileException(99, f'Config file permissions denied: {config_path}')
    except Exception as err:
        raise ConfigBaseException(99, str(err)) from err


def create_config(config_path: Path, encoding: str = 'utf-8') -> None:
    try:
        with config_path.open('w', encoding=encoding) as f:
            f.write(config_string)
    except PermissionError as err:
        raise ConfigFileException(99, f'Config file permissions denied: {config_path}')
    except Exception as err:
        raise ConfigBaseException(99, str(err)) from err
