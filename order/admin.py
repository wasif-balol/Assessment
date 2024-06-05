from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Order, OrderAdmin)
