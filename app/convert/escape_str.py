def escape_str(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    return string.replace('.', '\\.')

def unescape_str(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    return string.replace('\\.', '.')