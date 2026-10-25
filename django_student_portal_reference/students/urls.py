from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("<int:pk>/edit/", views.student_update, name="student_update"),
    path("<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("feedback/", views.feedback_list, name="feedback_list"),
    path("feedback/add/", views.feedback_create, name="feedback_create"),
    path("feedback/<int:pk>/delete/", views.feedback_delete, name="feedback_delete"),
]
