from typing import Any, Dict

class User:
    # ok: python-ban-any-in-domain-signatures
    def __eq__(self, other: object) -> bool:
        return isinstance(other, User)

# ruleid: python-ban-any-in-domain-signatures
def _first_relation_values(entity: Any | None) -> dict[str, object] | None:
    if not entity:
        return None
    return {}

# ruleid: python-ban-any-in-domain-signatures
def process_payload(data: Any) -> int:
    return 1

# ruleid: python-ban-any-in-domain-signatures
def process_object(data: object) -> int:
    return 1

# ruleid: python-ban-any-in-domain-signatures
def get_dynamic() -> Any:
    return None

# ruleid: python-ban-any-in-domain-signatures
def get_object() -> object:
    return None

# ruleid: python-ban-any-in-domain-signatures
def parse_dict(payload: dict[str, Any]) -> str:
    return "ok"

# ruleid: python-ban-any-in-domain-signatures
def parse_object_dict(payload: dict[str, object]) -> str:
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
