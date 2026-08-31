from decimal import Decimal


def from_decimal(value: Decimal) -> float:
    return float(value)

def to_decimal(value: float) -> Decimal:
    return Decimal(str(value))