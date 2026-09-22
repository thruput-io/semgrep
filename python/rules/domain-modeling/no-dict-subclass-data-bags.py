from typing import Dict
from dataclasses import dataclass

# ruleid: python-no-dict-subclass-data-bags
class TokenClaims(dict[str, str | int | float | bool | list[str]]):
    pass

# ruleid: python-no-dict-subclass-data-bags
class LegacyClaims(Dict[str, str]):
    pass

# ruleid: python-no-dict-subclass-data-bags
class UntypedBag(dict):
    pass

# ok: python-no-dict-subclass-data-bags
@dataclass(frozen=True)
class StronglyTypedTokenClaims:
    subject: str
    issuer: str
    expiration: int
    roles: list[str]

# ok: python-no-dict-subclass-data-bags
class StandardDomainEntity:
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
