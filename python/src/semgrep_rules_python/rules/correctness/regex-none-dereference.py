import re

def extract_token(header: str):
    # ruleid: python-regex-none-dereference
    token1 = re.search(r"Bearer (\w+)", header).group(1)

    # ruleid: python-regex-none-dereference
    token2 = re.match(r"Bearer (\w+)", header).groups()

    # ok: python-regex-none-dereference
    if match := re.search(r"Bearer (\w+)", header):
        safe_token1 = match.group(1)

    # ok: python-regex-none-dereference
    match_obj = re.match(r"Bearer (\w+)", header)
    if match_obj is not None:
        safe_token2 = match_obj.groups()

    return token1, token2
