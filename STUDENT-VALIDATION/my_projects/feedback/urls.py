from django.urls import path
from .views import dashboard, view_feedback, submit_feedback


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('submit/', submit_feedback, name='submit_feedback'),
    path('view/', view_feedback, name='view_feedback'),
]