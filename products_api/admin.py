from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register((Product))
class ProductAdmin(admin.ModelAdmin):
    """change view of panel admin"""
    list_display = ('name', 'price', 'count', 'available')
    list_filter = ('name', 'count')
    list_editable = ('available', 'count')  # this field can edit in list of product in panel admin


admin.site.register(Order)
admin.site.register(OrderItem)
