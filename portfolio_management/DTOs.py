from dataclasses import dataclass

from helpers.enums import ExchangeType


@dataclass
class OrderDTO:
    uuid: str
    abbreviation: str
    amount: float
    exchange: ExchangeType
