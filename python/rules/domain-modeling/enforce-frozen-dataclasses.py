from dataclasses import dataclass

# ruleid: python-enforce-frozen-dataclasses
@dataclass
class MutableUser:
    id: str
    name: str

# ruleid: python-enforce-frozen-dataclasses
@dataclass(order=True)
class MutableOrder:
    order_id: int

# ok: python-enforce-frozen-dataclasses
@dataclass(frozen=True)
class ImmutableUser:
    id: str
    name: str

# ok: python-enforce-frozen-dataclasses
@dataclass(frozen=True, slots=True)
class ImmutableOrder:
    order_id: int
