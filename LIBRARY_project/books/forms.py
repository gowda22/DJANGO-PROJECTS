from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BorrowingForm(forms.Form):
    borrowing_days = forms.IntegerField(
        min_value=1,
        max_value=30,
        initial=14,
        label="Borrowing period (days)",
        help_text="Choose between 1 and 30 days.",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 30}),
    )


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
