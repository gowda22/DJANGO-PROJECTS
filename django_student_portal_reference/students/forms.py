from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import transaction

from .models import Feedback, Student

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Create Django credentials and the matching Student profile."""

    email = forms.EmailField(required=True)
    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z][A-Za-z .'-]*$",
                message="Use letters, spaces, apostrophes, dots, or hyphens in the name.",
            )
        ],
    )
    course = forms.ChoiceField(choices=Student.COURSE_CHOICES)
    age = forms.IntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(100)]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must contain at least 2 characters.")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        if Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A student profile with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            # Keep account and profile creation together as one database transaction.
            with transaction.atomic():
                user.save()
                Student.objects.create(
                    user=user,
                    name=self.cleaned_data["name"],
                    email=self.cleaned_data["email"],
                    course=self.cleaned_data["course"],
                    age=self.cleaned_data["age"],
                )
        return user


class StudentUpdateForm(forms.ModelForm):
    """Edit profile details, not the user's login password or username."""

    class Meta:
        model = Student
        fields = ["name", "email", "course", "age"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must contain at least 2 characters.")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        duplicates = Student.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError("Another student already uses this email.")
        other_user = User.objects.filter(email__iexact=email).exclude(pk=self.instance.user_id)
        if other_user.exists():
            raise forms.ValidationError("Another account already uses this email.")
        return email

    # Override clean() when one validation rule depends on more than one field.
    # Example: compare course and age in cleaned_data and raise ValidationError
    # or call self.add_error("age", "..."), based on your real requirement.


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 5:
            raise forms.ValidationError("Feedback must contain at least 5 characters.")
        return message
