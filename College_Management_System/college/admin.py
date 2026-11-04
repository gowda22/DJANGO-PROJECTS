from django.contrib import admin
from .models import Department, Course, Student, Faculty, Attendance
admin.site.register([Department, Course, Student, Faculty, Attendance])
