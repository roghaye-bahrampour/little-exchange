from helpers.enums import ExchangeType
from portfolio_management.services.exchanges.kucoin import KucoinClient


class ExchangeClientFactory:

    @staticmethod
    def get_client(exchange: ExchangeType):
        if exchange == ExchangeType.KUCOIN:
            return KucoinClient()
        else:
            raise NotImplementedError(f'{exchange.value} is not available!')
