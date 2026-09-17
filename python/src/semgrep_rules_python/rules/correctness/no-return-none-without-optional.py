from typing import Optional, Union

class User:
    pass

# ruleid: python-no-return-none-without-optional
def find_user(user_id: int) -> User:
    if user_id <= 0:
        return None
    return User()

# ruleid: python-no-return-none-without-optional
def get_name(user_id: int) -> str:
    if user_id <= 0:
        return None
    return "Alice"

# ruleid: python-no-return-none-without-optional
def calculate_score(val: int) -> int:
    if val < 0:
        return None
    return val * 10

# ok: python-no-return-none-without-optional
def find_user_safe(user_id: int) -> Optional[User]:
    if user_id <= 0:
        return None
    return User()

# ok: python-no-return-none-without-optional
def find_user_pipe_syntax(user_id: int) -> User | None:
    if user_id <= 0:
        return None
    return User()

# ok: python-no-return-none-without-optional
def find_user_union(user_id: int) -> Union[User, None]:
    if user_id <= 0:
        return None
    return User()

# ok: python-no-return-none-without-optional
def reset_state() -> None:
    return None
