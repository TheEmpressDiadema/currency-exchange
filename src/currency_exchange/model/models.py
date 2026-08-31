from dataclasses import dataclass, field

from currency_exchange.model.value_objects import Code, Name, Rate, Sign


@dataclass
class Currency:

    code: Code
    name: Name
    sign: Sign
    id: int | None = field(default=None)

@dataclass
class ExchangeRate:

    base_currency: Currency
    target_currency: Currency
    rate: Rate
    id: int | None = field(default=None)