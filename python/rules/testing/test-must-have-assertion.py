import pytest

# ruleid: python-test-must-have-assertion
def test_no_assert():
    x = 10
    y = 20
    z = x + y

# ok: python-test-must-have-assertion
def test_with_assert():
    assert 1 + 1 == 2

# ok: python-test-must-have-assertion
def test_with_pytest_raises():
    with pytest.raises(ValueError):
        int("invalid")

# ok: python-test-must-have-assertion
def non_test_helper():
    x = 10
