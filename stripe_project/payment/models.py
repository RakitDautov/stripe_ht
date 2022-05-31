from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(
        Item,
        through='ItemsInOrder',
        related_name='order',
        blank=True,
        verbose_name='Вещи в корзине'
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class ItemsInOrder(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='Вещи',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Корзина'
    )
    amount = models.PositiveIntegerField(
        null=True,
        verbose_name='Количество вещей'
    )
