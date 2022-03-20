from asyncio.log import logger
from base64 import encode
from dataclasses import dataclass
from ensurepip import version
from typing import Any, Dict


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
    root: Dict[str, Any]
    loggers: Dict[str, Any]
    handlers: Dict[str, Any]
    formatters: Dict[str, Any]

@dataclass
class Config():
    name: str
    presets: Dict[str, ConfigApp]
    logging: ConfigLogging