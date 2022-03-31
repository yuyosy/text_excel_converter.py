from dataclasses import dataclass
from typing import Any, Dict, Union


@dataclass
class ConfigDefinitions():
    folder: str
    file_pattern: str
    version: str
    encoding: str


@dataclass
class ConfigTemplates():
    folder: str
    file_pattern: str

@dataclass
class ConfigAppOptions():
    definitions: ConfigDefinitions
    templates: ConfigTemplates


@dataclass
class ConfigApp():
    name: str
    description: str
    options: ConfigAppOptions

@dataclass
class ConfigLogging():
    version: int
    root: Union[Dict[str, Any], None]
    loggers: Dict[str, Any]
    handlers: Dict[str, Any]
    formatters: Dict[str, Any]

@dataclass
class Config():
    name: str
    presets: Dict[str, ConfigApp]
    logging: ConfigLogging
