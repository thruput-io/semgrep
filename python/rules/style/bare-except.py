def handle_data(raw):
    # ruleid: python-bare-except
    try:
        val = int(raw)
    except:
        val = 0

    # ok: python-bare-except
    try:
        val2 = int(raw)
    except ValueError:
        val2 = 0

    # ok: python-bare-except
    try:
        val3 = int(raw)
    except Exception:
        val3 = 0

    return val, val2, val3
