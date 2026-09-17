import pytest
import unittest

# ruleid: python-no-skipped-or-ignored-tests
@pytest.mark.skip(reason="WIP")
def test_skipped():
    assert True

# ruleid: python-no-skipped-or-ignored-tests
@pytest.mark.skipif(True, reason="Conditional")
def test_skipif():
    assert True

# ruleid: python-no-skipped-or-ignored-tests
@unittest.skip("Not ready")
def test_unittest_skip():
    assert True

def test_inline_skip():
    # ruleid: python-no-skipped-or-ignored-tests
    pytest.skip("Skip inside body")

# ok: python-no-skipped-or-ignored-tests
def test_valid_active_test():
    assert 1 + 1 == 2
