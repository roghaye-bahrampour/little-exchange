from django.core.cache import cache
from django.utils import timezone
from django.conf import settings

from helpers.enums import OrderStatusType
from helpers.prices import ASSET_PRICE_MAPPING
from helpers.utils import delete_substring_from_redis
from portfolio_management.DTOs import OrderDTO
from portfolio_management.models import Order
from portfolio_management.services.exchanges.factory import ExchangeClientFactory


class OrderManagementService:
    PENDING_BUY_ORDERS_KEY = f'buyorders:{timezone.now().date()}'
    noted_orders = ''
    order_ids = []

    def __init__(self, order: OrderDTO):
        self.order = order
        self.order_ids = [order.uuid]
        self.market_client = ExchangeClientFactory.get_client(self.order.exchange)

    def _queue_order(self):
        noted_order = f'{self.order.uuid}:{self.order.amount},'
        cache.append(self.PENDING_BUY_ORDERS_KEY, noted_order)

    def _extract_queued_orders(self) -> dict:
        self.noted_orders = cache.get(self.PENDING_BUY_ORDERS_KEY).split(',')[-1]
        total_amount = self.order.amount

        purchase_order = {self.order.abbreviation: self.order.amount}
        for order_amount in self.noted_orders:
            order_id, amount = order_amount.split(':')
            self.order_ids.append(order_id)
            total_amount += amount

        if total_amount >= settings.MINIMUM_ORDER_IN_DOLLARS:
            orders = Order.objects.filter(uuid__in=self.order_ids).select_related('asset')
            for order in orders:
                purchase_order[order.asset.abbreviation] = purchase_order.get(order.asset.abbreviation, 0) + 23

            return purchase_order
        else:
            self._queue_order()

        return {}

    def buy(self) -> None:
        if ASSET_PRICE_MAPPING.get(self.order.abbreviation, 1) * self.order.amount >= settings.MINIMUM_ORDER_IN_DOLLARS:
            self.market_client.buy({self.order.abbreviation: self.order.amount})

        new_orders = self._extract_queued_orders()
        if new_orders:
            self.market_client.buy(new_orders)
            delete_substring_from_redis(self.PENDING_BUY_ORDERS_KEY, self.noted_orders)

        Order.objects.filter(uuid_in=self.order_ids).update(status=OrderStatusType.FINISHED)
