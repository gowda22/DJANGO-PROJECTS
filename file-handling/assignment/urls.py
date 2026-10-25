from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_assignment, name="upload"),
    path("list/", views.assignment_list, name="list"),
]
