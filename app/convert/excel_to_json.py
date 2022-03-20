# import json
# from pathlib import Path


# class ToJson():
#     def write_json(self, path: Path, *, encoding='utf-8'):
#         path.parent.mkdir(parents=True, exist_ok=True)
#         with path.open('w', encoding=encoding) as f:
#             f.write(json.dumps(self.data.asattrdict(), indent=4, ensure_ascii=False, default=str))
