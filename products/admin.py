from django.contrib import admin

# Register your models here.
from .models import Product, OrderProductRelation, Order

admin.site.register(Product)
admin.site.register(OrderProductRelation)
admin.site.register(Order)
