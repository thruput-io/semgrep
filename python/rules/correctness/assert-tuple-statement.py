def validate(x):
    # ruleid: python-assert-tuple-statement
    assert (x > 0, "x must be positive")

    # ruleid: python-assert-tuple-statement
    assert (x is not None, "must not be None")

    # ok: python-assert-tuple-statement
    assert x > 0, "x must be positive"

    # ok: python-assert-tuple-statement
    assert x is not None
