from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.IntegerField()
    description = models.TextField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0

    def borrow_book(self):
        """Reduce the available count by one when at least one copy remains."""
        if self.available_copies <= 0:
            return False
        self.available_copies -= 1
        self.save(update_fields=["available_copies"])
        return True

    def return_book(self):
        """Restore one copy, without allowing the count to exceed inventory."""
        if self.available_copies >= self.total_copies:
            return False
        self.available_copies += 1
        self.save(update_fields=["available_copies"])
        return True


class Borrowing(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    borrowed_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["-borrowed_date"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def is_overdue(self):
        """Return True while an unreturned borrowing is past its due date."""
        return self.returned_date is None and timezone.now() > self.due_date

    def calculate_fine(self):
        """Calculate $1 per full day late, using the return date if returned."""
        end_date = self.returned_date or timezone.now()
        if end_date <= self.due_date:
            return Decimal("0.00")
        days_overdue = (end_date - self.due_date).days
        return Decimal(days_overdue) * Decimal("1.00")

    def save(self, *args, **kwargs):
        # Keep overdue status current whenever this record is saved.
        if self.returned_date is None and self.due_date and timezone.now() > self.due_date:
            self.status = "overdue"
            self.fine_amount = self.calculate_fine()
        super().save(*args, **kwargs)
