from django.db import models


class AssetType(models.IntegerChoices):
    COIN = 0, 'coin'
    TOKEN = 1, 'token'


class OrderStatusType(models.IntegerChoices):
    RESERVED = 0, 'reserved'
    QUEUED = 1, 'queued'
    IN_PROCESS = 2, 'in_process'
    FINISHED = 3, 'finished'
    FAILED = 4, 'failed'
    SCHEDULED = 5, 'scheduled'


class ExchangeType(models.IntegerChoices):
    ABAN = 0, 'aban'
    KUCOIN = 1, 'kucoin'
    COINEX = 2, 'coinex'
