from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("student_name", "course", "assignment_file", "submitted_on")
    list_filter = ("course", "submitted_on")
    search_fields = ("student_name", "course")
    readonly_fields = ("submitted_on",)
