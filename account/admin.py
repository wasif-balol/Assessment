from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active', 'is_admin',)
    readonly_fields = ('is_active', 'is_admin',)


admin.site.register(User, UserAdmin)
