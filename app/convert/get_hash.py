
import hashlib
import json
from typing import Dict, List, Union


def get_json_hash(data: Union[Dict, List], *, name='sha256') -> str:
    hash = hashlib.new(name, json.dumps(data, ensure_ascii=False, default=str).encode())
    return hash.hexdigest()