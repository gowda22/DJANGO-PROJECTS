from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CoustomUser


@admin.register(CoustomUser)
class CoustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Application Role', {
            'fields': ('role',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Application Role', {
            'fields': ('role',)
        }),
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
    )