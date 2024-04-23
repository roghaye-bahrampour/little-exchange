from celery import shared_task

from helpers.enums import ExchangeType
from portfolio_management.DTOs import OrderDTO
from portfolio_management.services.order import OrderManagementService


@shared_task
def buy_product_on_third_party(abbreviation: str, exchange: ExchangeType, amount: float, uuid: str):
    OrderManagementService(
        OrderDTO(uuid=uuid, abbreviation=abbreviation, amount=amount, exchange=exchange)
    ).buy()
