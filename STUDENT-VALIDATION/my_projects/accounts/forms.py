from django.contrib.auth.forms import UserCreationForm
from .models import CoustomUser


class RigisterForm(UserCreationForm):

    class Meta:
        model = CoustomUser

        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]