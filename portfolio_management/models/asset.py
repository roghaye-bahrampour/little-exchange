from django.db import models

from helpers.model.base import BaseModel
from helpers.enums import AssetType, ExchangeType


class Asset(BaseModel):
    name = models.CharField(max_length=256, editable=False)
    abbreviation = models.CharField(max_length=32, editable=False, unique=True)
    category = models.PositiveSmallIntegerField(
        choices=AssetType.choices,
        default=AssetType.COIN.value,
        db_index=True
    )
    exchange = models.PositiveSmallIntegerField(
        choices=ExchangeType.choices,
        default=ExchangeType.KUCOIN.value,
        db_index=True
    )

    def __str__(self):
        return self.abbreviation
