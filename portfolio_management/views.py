from rest_framework import viewsets

from portfolio_management.models import Order
from portfolio_management.serializers import OrderSerializer, BuyAssetSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def initial(self, request, *args, **kwargs):
        super(OrderViewSet, self).initial(request, *args, **kwargs)
        self.request.data['client'] = self.request.user.id

    def get_serializer_class(self):
        serializer_class = {
            'create': BuyAssetSerializer,
        }
        return serializer_class.get(self.action) or OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    