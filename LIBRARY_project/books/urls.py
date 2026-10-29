from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("book/<int:book_id>/borrow/", views.borrow_book, name="borrow_book"),
    path("borrowing/<int:borrowing_id>/return/", views.return_book, name="return_book"),
    path("my-borrowings/", views.user_borrowings, name="user_borrowings"),
    path("author/<int:author_id>/", views.author_detail, name="author_detail"),
    path("register/", views.register, name="register"),
]
