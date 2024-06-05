from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "stock", 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Product, ProductAdmin)
