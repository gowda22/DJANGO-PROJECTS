
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Homepage redirects to login
    path(
        '',
        RedirectView.as_view(
            url='/accounts/login/',
            permanent=False
        ),
        name='home'
    ),

    # Admin
    path('admin/', admin.site.urls),

    # Registration, login and logout
    path('accounts/', include('accounts.urls')),

    # Dashboard, submit feedback and view feedback
    path('', include('feedback.urls')),
]
