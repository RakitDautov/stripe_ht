from django.contrib import admin

from .models import Item, Order

admin.site.register(Item)


class ItemsInOrder(admin.TabularInline):
    model = Order.items.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemsInOrder,
    ]
