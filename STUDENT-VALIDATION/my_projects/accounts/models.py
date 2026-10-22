from django.db import models
from django.contrib.auth.models import AbstractUser


# Create custom user
class CoustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )