from django.urls import path
from . import views
urlpatterns = [
 path("", views.dashboard, name="dashboard"),
 path("departments/", views.departments, name="departments"),
 path("departments/add/", views.department_add, name="department_add"),
 path("departments/<int:pk>/edit/", views.department_edit, name="department_edit"),
 path("departments/<int:pk>/delete/", views.department_delete, name="department_delete"),
 path("courses/", views.courses, name="courses"),
 path("courses/add/", views.course_add, name="course_add"),
 path("courses/<int:pk>/edit/", views.course_edit, name="course_edit"),
 path("courses/<int:pk>/delete/", views.course_delete, name="course_delete"),
 path("students/", views.students, name="students"),
 path("students/add/", views.student_add, name="student_add"),
 path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
 path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
 path("faculty/", views.faculty, name="faculty"),
 path("faculty/add/", views.faculty_add, name="faculty_add"),
 path("faculty/<int:pk>/edit/", views.faculty_edit, name="faculty_edit"),
 path("faculty/<int:pk>/delete/", views.faculty_delete, name="faculty_delete"),
 path("attendance/", views.attendance, name="attendance"),
 path("attendance/add/", views.attendance_add, name="attendance_add"),
 path("attendance/<int:pk>/delete/", views.attendance_delete, name="attendance_delete"),
]
