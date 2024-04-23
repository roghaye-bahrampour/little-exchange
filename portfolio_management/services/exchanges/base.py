from portfolio_management.DTOs import OrderDTO


class BaseMarketActionService:

    def buy(self, order: OrderDTO) -> None:
        pass

    def sell(self, order: OrderDTO) -> None:
        pass
