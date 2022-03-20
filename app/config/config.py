from pathlib import Path

from ruamel.yaml import YAML
from dacite.core import from_dict

from .config_class import Config
from .const import config_string


def init_config(config_path: Path, encoding:str='utf-8') -> Config:
    create_config(config_path, encoding) # ------------- DEBUG
    if not config_path.exists():
        create_config(config_path, encoding)
    return load_config(config_path, encoding)


def load_config(config_path: Path, encoding:str='utf-8') -> Config:
    yaml=YAML(typ="safe")
    with config_path.open('r', encoding=encoding) as f:
        config_data = yaml.load(f)
    return from_dict(data_class=Config, data=config_data)


def create_config(config_path: Path, encoding:str='utf-8') -> None:
    with config_path.open('w', encoding=encoding) as f:
        f.write(config_string)
