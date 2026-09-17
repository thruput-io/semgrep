def parse_name(name: str):
    # ruleid: python-falsy-empty-string-check
    clean = name or "Anonymous"
    return clean

def parse_name_safe(name: str):
    # ok: python-falsy-empty-string-check
    clean = "Anonymous" if name is None else name
    return clean
