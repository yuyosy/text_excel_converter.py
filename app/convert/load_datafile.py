import json
from pathlib import Path
from typing import Any, Dict


def load_textfile(file:Path) -> Dict[str, Any]:
    data = {}
    if file.suffix in ['.json']:
        with file.open('r', encoding='utf-8') as f:
            data = json.load(f)
    return data
