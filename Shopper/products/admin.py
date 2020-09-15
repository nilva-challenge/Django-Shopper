from django.contrib import admin
from .models import product, Order, OrderItem
# Register your models here.

admin.site.register(product)
admin.site.register(Order)
admin.site.register(OrderItem)