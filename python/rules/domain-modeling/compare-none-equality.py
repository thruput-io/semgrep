def check_values(val):
    # ruleid: python-compare-none-equality
    if val == None:
        return False

    # ruleid: python-compare-none-equality
    if val != None:
        return True

    # ruleid: python-compare-none-equality
    if None == val:
        return False

    # ruleid: python-compare-none-equality
    if None != val:
        return True

    # ok: python-compare-none-equality
    if val is None:
        return False

    # ok: python-compare-none-equality
    if val is not None:
        return True

    return True
