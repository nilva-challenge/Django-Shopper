from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'count', 'order_date', )
    search_fields = ('user', 'product', )
    ordering = ('-order_date', )
