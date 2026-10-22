from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'message',
        'created_at',
    )

    search_fields = (
        'user__username',
        'message',
    )

    list_filter = ('created_at',)

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)

    list_per_page = 25