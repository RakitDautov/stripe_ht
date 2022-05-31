from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import stripe
from django.conf import settings

from .models import Item, Order, ItemsInOrder
from .serializers import ItemSerializer, CreateOrderSerializer, ShowOrderSerializer


class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowOrderSerializer
        return CreateOrderSerializer


def form_items_fill(order):
    items = ItemsInOrder.objects.filter(order=order)
    data = []
    for i in items:
        form = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': i.item.name
                },
                'unit_amount': i.item.price*100
            },
            'quantity': i.amount,
        }
        data.append(form)
    return data


@api_view(['GET'])
def create_checkout(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = Order.objects.get(pk=pk)
    data = form_items_fill(order)
    session = stripe.checkout.Session.create(
        line_items=data,
        mode='payment',
        success_url='https://127.0.0.1/order/',
        cancel_url='https://127.0.0.1/order/',
    )

    return Response(session.url)
