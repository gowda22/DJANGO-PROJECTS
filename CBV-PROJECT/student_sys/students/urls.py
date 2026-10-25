from django .urls import path
from .views import *
urlpattrens=[
    path("",StudentListView(),name="student-list"),
    path("student/<int:pk/",StudentDetailsView(),name="student-details"),
    path("create/",StudentCreateView(),name="student-create"),
    path("update/<int:pk",StudentUpdateView),
]

