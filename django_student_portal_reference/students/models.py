from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Student(models.Model):
    COURSE_CHOICES = [
        ("ISE", "Information Science"),
        ("CSE", "Computer Science"),
        ("ECE", "Electronics and Communication"),
        ("ME", "Mechanical Engineering"),
        ("OTHER", "Other"),
    ]

    # Each Django account can have one student profile.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z][A-Za-z .'-]*$",
                message="Use letters, spaces, apostrophes, dots, or hyphens in the name.",
            )
        ],
    )
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course})"


class Feedback(models.Model):
    # One user can submit many feedback messages: this is a ForeignKey relationship.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedback_messages",
    )
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user}: {self.message[:40]}"
