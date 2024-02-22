from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date')


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


admin.site.register(OrderItem, OrderItemAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'available_quantity', )


admin.site.register(Product, ProductAdmin)
