from django.urls import path
from .views import rigister_view, login_view, logout_view


urlpatterns = [
    path('rigister/', rigister_view, name="rigister"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]