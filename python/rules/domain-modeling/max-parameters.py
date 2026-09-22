from typing import List
from typing_extensions import override

# ok: python-max-parameters-warning
# ok: python-max-parameters-error
def calculate_sum(a: int, b: int) -> int:
    return a + b

# ruleid: python-max-parameters-warning
def build_point(x: float, y: float, z: float) -> tuple:
    return (x, y, z)

# ruleid: python-max-parameters-error
def create_user(name: str, email: str, age: int, role: str) -> dict:
    return {"name": name, "email": email, "age": age, "role": role}

class BaseCustomerController:
    pass

class CustomerController(BaseCustomerController):
    # ok: python-max-parameters-warning
    # ok: python-max-parameters-error
    def __init__(self, a: str, b: str, c: str, d: str, e: str):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    # ok: python-max-parameters-warning
    # ok: python-max-parameters-error
    def find_user(self, user_id: str, tenant_id: str) -> str:
        return user_id

    # ruleid: python-max-parameters-warning
    def update_user(self, user_id: str, first_name: str, last_name: str) -> str:
        return user_id

    # ruleid: python-max-parameters-error
    def register_user(self, username: str, email: str, address: str, phone: str) -> str:
        return username

    # ok: python-max-parameters-warning
    # ok: python-max-parameters-error
    @override
    async def search_customers(
        self,
        dot_number: str,
        name: str,
        street: str,
        zip: str,
        city: str,
        state: str,
        country: str,
    ) -> List[str]:
        return []

    # ok: python-max-parameters-warning
    # ok: python-max-parameters-error
    @override
    def filter_triadic(self, a: str, b: str, c: str) -> str:
        return a
