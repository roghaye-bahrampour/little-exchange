from django.contrib.auth.models import User
from django.db import models

from portfolio_management.models.asset import Asset
from helpers.model.base import BaseModel


class Portfolio(BaseModel):

    client = models.ForeignKey(User, related_name='portfolio', on_delete=models.PROTECT)
    asset = models.ManyToManyField(Asset, related_name='portfolios')
    amount = models.FloatField(default=0)
