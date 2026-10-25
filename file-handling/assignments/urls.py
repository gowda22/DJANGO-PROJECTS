from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path("", views.assignment_list, name="list"),
    path("upload/", views.upload_assignment, name="upload"),
]
