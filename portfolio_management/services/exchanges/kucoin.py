from portfolio_management.DTOs import OrderDTO
from portfolio_management.services.exchanges.base import BaseMarketActionService


class KucoinClient(BaseMarketActionService):

    def buy(self, coin_amount: dict = {}) -> None:
        pass
