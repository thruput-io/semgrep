def test_user_creation_with_branches():
    # ruleid: python-no-branching-or-loops-in-tests
    if True:
        user = "Alice"

    # ruleid: python-no-branching-or-loops-in-tests
    for i in range(3):
        assert i >= 0

    # ruleid: python-no-branching-or-loops-in-tests
    try:
        val = int("123")
    except ValueError:
        val = 0

def test_linear_deterministic():
    # ok: python-no-branching-or-loops-in-tests
    user = "Alice"
    assert user == "Alice"

def helper_function(condition):
    # ok: python-no-branching-or-loops-in-tests
    if condition:
        return 1
    return 0
