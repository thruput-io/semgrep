class CustomerId:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CustomerId) and self.value == other.value

def check_same_customer(a: CustomerId, b: CustomerId) -> bool:
    # ruleid: python-no-unwrapping-domain-primitives
    return a.value == b.value

def check_different_customer(a: CustomerId, b: CustomerId) -> bool:
    # ruleid: python-no-unwrapping-domain-primitives
    return a.value != b.value

def check_safe_customer(a: CustomerId, b: CustomerId) -> bool:
    # ok: python-no-unwrapping-domain-primitives
    return a == b
