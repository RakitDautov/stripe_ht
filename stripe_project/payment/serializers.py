from rest_framework import serializers
from .models import Item, Order, ItemsInOrder


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price']


class ItemInOrderSerializer(serializers.ModelSerializer):

    name = serializers.SlugRelatedField(
        source='item',
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = ItemsInOrder
        fields = ['name', 'amount']


class AddItemsToOrderSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
    )

    class Meta:
        model = ItemsInOrder
        fields = ['id', 'amount']


class ShowOrderSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Order
        fields = ['id', 'items']

    def get_items(self, obj):
        items = ItemsInOrder.objects.filter(order=obj)
        return ItemInOrderSerializer(items, many=True).data


class CreateOrderSerializer(serializers.ModelSerializer):

    items = AddItemsToOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items', ]
