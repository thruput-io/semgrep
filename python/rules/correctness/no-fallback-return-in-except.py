def fetch_config():
    # ruleid: python-no-fallback-return-in-except
    try:
        val = int("invalid")
    except ValueError:
        return {}

def check_status():
    # ruleid: python-no-fallback-return-in-except
    try:
        val = int("invalid")
    except Exception:
        return False

def safe_handling():
    # ok: python-no-fallback-return-in-except
    try:
        val = int("123")
        return val
    except ValueError as exc:
        raise RuntimeError("Parsing failed") from exc
