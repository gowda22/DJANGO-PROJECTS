from django.contrib import admin
from .models import Feedback, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "course", "age", "user", "created_at")
    search_fields = ("name", "email", "user__username")
    list_filter = ("course",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at")
    search_fields = ("user__username", "message")
    list_filter = ("created_at",)
