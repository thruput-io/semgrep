# type: ignore
# noqa
# pragma: no cover
def calculate_tax(amount: float) -> float:
    # ruleid: python-no-comments
    # calculate 20 percent VAT rate
    rate = 0.20
    return amount * rate

def calculate_discount(price: float) -> float:
    # ok: python-no-comments
    # type: ignore
    return price * 0.9
