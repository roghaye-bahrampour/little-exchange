from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from helpers.enums import OrderStatusType
from helpers.prices import ASSET_PRICE_MAPPING
from portfolio_management.models import Order, Portfolio, Asset
from portfolio_management.tasks import buy_product_on_third_party


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class BuyAssetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'uuid',
            'cost',
            'asset',
            'status',
            'created',
            'modified'
        )

    def validate(self, data):
        print(data)
        print(data.get('amount')*ASSET_PRICE_MAPPING.get(data.get('name')))
        if ASSET_PRICE_MAPPING.get(data.get('name')) is None:
            raise serializers.ValidationError('Invalid asset name.')

        if not Portfolio.objects.filter(
                client_id=data.get('client'),
                asset__abbreviation='DOLLAR',
                amount__gte=data.get('amount')*ASSET_PRICE_MAPPING.get(data.get('name'))).exists():
            raise serializers.ValidationError('Not enough amount of asset')

        return data

    def create(self, validated_data):
        product = Asset.objects.get(abbreviation=validated_data.get('name'))
        with transaction.atomic():
            Portfolio.objects.filter(
                client_id=validated_data.get('client'),
                asset=product,
            ).update(amount=F('amount')-validated_data.get('amount'))
            order = Order.objects.create(
                client=validated_data.get('client'),
                cost=validated_data.get('amount')*ASSET_PRICE_MAPPING.get(product.abbreviation),
                asset=product,
                amount=validated_data.get('amount'),
                status=OrderStatusType.QUEUED
            )
            order.asset.set([product.id])

        buy_product_on_third_party.apply_async(
            args=(order.asset.abbreviation, order.asset.exchange, order.amount, order.uuid,),
            queue='spot_buy'
        )

        return order

