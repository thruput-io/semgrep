import re

def process_logs(logs):
    # ruleid: python-repeated-regex-compile
    for log in logs:
        pattern = re.compile(r"ERROR:\s+(.*)")
        match = pattern.search(log)

    # ok: python-repeated-regex-compile
    safe_pattern = re.compile(r"ERROR:\s+(.*)")
    for log in logs:
        match = safe_pattern.search(log)
