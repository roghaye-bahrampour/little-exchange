from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from helpers.enums import OrderStatusType
from helpers.prices import ASSET_PRICE_MAPPING
from portfolio_management.models import Order, Portfolio
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
        if ASSET_PRICE_MAPPING.get(data.get('name')) is None:
            raise serializers.ValidationError('Invalid asset name.')

        if not Portfolio.objects.filter(
                client_id=data.get('user'),
                asset__abbreviation='DOLLAR',
                amount__gte=data.get('amount')*ASSET_PRICE_MAPPING.get(data.get('name'))).exists():
            raise serializers.ValidationError('Not enough amount of asset')

        return data

    def create(self, validated_data):

        with transaction.atomic():
            product = validated_data.get('asset')
            Portfolio.objects.filter(
                client_id=validated_data.get('user'),
                asset=product,
            ).update(F('amount')-validated_data.get('amount'))
            order = Order.objects.create(
                client_id=validated_data.get('user'),
                asset__abbreviation=product,
                cost=validated_data.get('amount')*ASSET_PRICE_MAPPING.get(product),
                amount=validated_data.get('amount'),
                status=OrderStatusType.QUEUED
            )

        buy_product_on_third_party.apply_async(
            args=(order.asset.abbreviation, order.asset.exchange, order.amount, order.uuid,),
            queue='spot_buy'
        )

        return order

