from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BorrowingForm, UserRegistrationForm
from .models import Author, Book, Borrowing


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect("books:book_list")
    else:
        form = UserRegistrationForm()
    return render(request, "books/register.html", {"form": form})


def book_list(request):
    books = Book.objects.select_related("author").all()
    search_query = request.GET.get("search", "").strip()
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query)
            | Q(author__name__icontains=search_query)
            | Q(isbn__icontains=search_query)
        )

    availability = request.GET.get("availability", "")
    if availability == "available":
        books = books.filter(available_copies__gt=0)

    return render(
        request,
        "books/book_list.html",
        {"books": books, "search_query": search_query, "availability": availability},
    )


def book_detail(request, book_id):
    book = get_object_or_404(Book.objects.select_related("author"), id=book_id)
    return render(request, "books/book_detail.html", {"book": book})


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    existing_borrowing = Borrowing.objects.filter(
        user=request.user, book=book, status__in=["active", "overdue"]
    ).exists()
    if existing_borrowing:
        messages.error(request, "You already have this book borrowed.")
        return redirect("books:book_detail", book_id=book.id)

    if request.method == "POST":
        form = BorrowingForm(request.POST)
        if form.is_valid():
            # Lock the book row while checking and updating the available-copy count.
            with transaction.atomic():
                locked_book = Book.objects.select_for_update().get(pk=book.pk)
                already_borrowed = Borrowing.objects.filter(
                    user=request.user,
                    book=locked_book,
                    status__in=["active", "overdue"],
                ).exists()
                if already_borrowed:
                    messages.error(request, "You already have this book borrowed.")
                    return redirect("books:book_detail", book_id=locked_book.id)
                if locked_book.available_copies <= 0:
                    messages.error(request, "This book is no longer available.")
                    return redirect("books:book_detail", book_id=locked_book.id)

                locked_book.available_copies -= 1
                locked_book.save(update_fields=["available_copies"])
                due_date = timezone.now() + timedelta(days=form.cleaned_data["borrowing_days"])
                Borrowing.objects.create(user=request.user, book=locked_book, due_date=due_date)

            messages.success(request, f'Successfully borrowed "{book.title}".')
            return redirect("books:user_borrowings")
    else:
        form = BorrowingForm()

    return render(request, "books/borrow_book.html", {"book": book, "form": form})


@login_required
def return_book(request, borrowing_id):
    borrowing = get_object_or_404(
        Borrowing.objects.select_related("book", "book__author"),
        id=borrowing_id,
        user=request.user,
    )

    if request.method == "POST":
        if borrowing.status == "returned":
            messages.info(request, "This book has already been returned.")
            return redirect("books:user_borrowings")

        # Calculate before marking the borrowing as returned.
        fine = borrowing.calculate_fine()
        borrowing.returned_date = timezone.now()
        borrowing.status = "returned"
        borrowing.fine_amount = fine
        borrowing.save()
        borrowing.book.return_book()
        messages.success(request, f'Successfully returned "{borrowing.book.title}".')
        return redirect("books:user_borrowings")

    return render(request, "books/return_book.html", {"borrowing": borrowing})


@login_required
def user_borrowings(request):
    active = request.user.borrowings.select_related("book", "book__author").filter(
        status__in=["active", "overdue"]
    )
    history = request.user.borrowings.select_related("book", "book__author").filter(
        status="returned"
    )[:10]
    return render(
        request,
        "books/user_borrowings.html",
        {"active_borrowings": active, "borrowing_history": history},
    )


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    return render(request, "books/author_detail.html", {"author": author, "books": books})


def custom_logout(request):
    """Kept for compatibility; the project URL uses Django's LogoutView."""
    logout(request)
    return redirect("books:book_list")
