from django.contrib import admin

# Register your models here.
from django.utils import timezone

from apps.product.models import Product


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    """
        Admin Panel For Products
    """
    list_display = ('id', 'name', 'is_exists')
    fields = ('id', 'name', 'is_exists')
    readonly_fields = ('id',)
    search_fields = ('name',)
    actions = [
        'is_exists',
        'not_exists'
    ]

    def is_exists(self, request, queryset):
        query_count = queryset.update(is_exists=True, update_datetime=timezone.now())
        self.message_user(request, f"{query_count} number of Products are now Available in shop")

    def not_exists(self, request, queryset):
        query_count = queryset.update(is_exists=False, update_datetime=timezone.now())
        self.message_user(request, f"{query_count} number of Products are now Available in shop")
