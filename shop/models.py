from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class Items(models.Model):
    name = models.CharField(max_length=256)
    price = models.FloatField()
    amount = models.BigIntegerField()

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'


class Orders(models.Model):
    user = models.ForeignKey(to=USER_MODEL, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(to=Items, on_delete=models.DO_NOTHING)
    amount = models.BigIntegerField()

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
