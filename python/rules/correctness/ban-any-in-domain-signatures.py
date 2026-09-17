from typing import Any, Dict

class User:
    pass

# ruleid: python-ban-any-in-domain-signatures
def process_payload(data: Any) -> int:
    return 1

# ruleid: python-ban-any-in-domain-signatures
def get_dynamic() -> Any:
    return None

# ruleid: python-ban-any-in-domain-signatures
def parse_dict(payload: dict[str, Any]) -> str:
    return "ok"

# ruleid: python-ban-any-in-domain-signatures
def fetch_raw() -> Dict[str, Any]:
    return {}

# ok: python-ban-any-in-domain-signatures
def process_user(user: User) -> str:
    return "ok"

# ok: python-ban-any-in-domain-signatures
def get_user_id() -> int:
    return 42
