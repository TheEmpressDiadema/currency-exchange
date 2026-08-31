from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ValueObject[T](ABC):

    value: T

    def __post_init__(self) -> None:
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        pass

@dataclass(frozen=True)
class Code(ValueObject[str]):

    value: str

    def _validate(self) -> None:
        if len(self.value) != 3:
            raise ValueError('Currency Code length not equals 3')

@dataclass(frozen=True)
class Name(ValueObject[str]):

    value: str

    def _validate(self) -> None:
        if len(self.value) not in range(4, 31):
            raise ValueError('Currency Name length should be in range of 4 and 31')

@dataclass(frozen=True)
class Sign(ValueObject[str]):

    value: str

    def _validate(self) -> None:
        l = len(self.value)
        if l > 2 or l == 0:
            raise ValueError('Currency Sign should be only one letter length')

@dataclass(frozen=True)
class Rate(ValueObject[Decimal]):

    value: Decimal

    def _validate(self) -> None:
        if self.value <= Decimal("0.0"):
            raise ValueError('Rate value should be higher than 0')