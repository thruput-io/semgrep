import pytest

# ruleid: python-no-test-case-ordering
@pytest.mark.order(1)
def test_first_step():
    assert 1 == 1

# ruleid: python-no-test-case-ordering
@pytest.mark.run(order=2)
def test_second_step():
    assert 2 == 2

# ok: python-no-test-case-ordering
def test_independent_step_a():
    assert 1 == 1

# ok: python-no-test-case-ordering
def test_independent_step_b():
    assert 2 == 2
