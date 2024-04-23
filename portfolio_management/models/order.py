from django.contrib.auth.models import User
from django.db import models

from portfolio_management.models.asset import Asset
from helpers.enums import OrderStatusType
from helpers.model.base import BaseModel


class Order(BaseModel):
    uuid = models.UUIDField(auto_created=True)
    client = models.ForeignKey(User, related_name='orders', on_delete=models.PROTECT)
    asset = models.ManyToManyField(Asset, related_name='orders', db_index=True)
    amount = models.FloatField()
    cost = models.FloatField()
    status = models.SmallIntegerField(
        choices=OrderStatusType.choices,
        default=OrderStatusType.RESERVED.value,
        db_index=True
    )

    def __str__(self):
        return self.uuid
