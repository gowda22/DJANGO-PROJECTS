from django.contrib import admin
from .models import Author, Book, Borrowing


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_date")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "available_copies", "total_copies")
    list_filter = ("author", "publication_year")
    search_fields = ("title", "isbn", "author__name")


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "borrowed_date", "due_date", "status", "fine_amount")
    list_filter = ("status", "borrowed_date")
    search_fields = ("user__username", "book__title")
