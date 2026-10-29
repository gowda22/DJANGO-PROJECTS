# Library Manager — Django Project

A Django-based library management project built from the code supplied for this task. It includes book and author catalogs, account registration/login, borrowing and returning books, an overdue-fine calculation, a borrowing-history page, Django admin screens, CSS styling, and a small JavaScript helper.

## Project structure

```text
LIBRARY_project/
├── manage.py
├── requirements.txt
├── README.md
├── LIBRARY_PROJECT/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── books/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
├── templates/
│   └── books/
│       ├── base.html
│       ├── book_list.html
│       ├── book_detail.html
│       ├── author_detail.html
│       ├── borrow_book.html
│       ├── login.html
│       ├── register.html
│       ├── return_book.html
│       └── user_borrowings.html
└── static/
    └── books/
        ├── css/style.css
        └── js/main.js
```

The initial database migration and `db.sqlite3` are intentionally not included. Generate the migration from the models on your computer using the commands below.

## Setup on Windows (VS Code / Command Prompt / PowerShell)

### 1. Extract the ZIP and open the project folder

Extract `LIBRARY_project.zip`. In VS Code, choose **File → Open Folder** and open the extracted `LIBRARY_project` folder — the folder containing `manage.py`.

Open the VS Code terminal (**Terminal → New Terminal**). Make sure the terminal is in the project root. You should see `manage.py` when you run `dir`.

### 2. Create a virtual environment

```powershell
py -m venv venv
```

If the `py` command is unavailable but Python is installed, use:

```powershell
python -m venv venv
```

### 3. Activate the environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Command Prompt (CMD):

```bat
venv\Scripts\activate.bat
```

After activation, the terminal usually shows `(venv)` at the start of the prompt. If PowerShell blocks activation due to execution policy, use Command Prompt or follow your organization's approved PowerShell policy guidance.

### 4. Install Django

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Confirm Django installed:

```powershell
python -m django --version
```

### 5. Check the project

```powershell
python manage.py check
```

If the check succeeds, continue to migrations.

### 6. Create and apply migrations

Run these commands from the same folder as `manage.py`:

```powershell
python manage.py makemigrations books
python manage.py migrate
```

`makemigrations` creates `books/migrations/0001_initial.py` from the app's models. `migrate` creates the local SQLite database and the tables for Django's built-in authentication/admin apps and this library app.

### 7. Create an administrator account

```powershell
python manage.py createsuperuser
```

Enter a username, optional email address, and password when prompted. The password will not visibly appear while typing; that is normal.

### 8. Start the development server

```powershell
python manage.py runserver
```

Open these pages in your browser:

- Catalog: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Registration: http://127.0.0.1:8000/register/
- Admin: http://127.0.0.1:8000/admin/

Keep the terminal running while using the website. Press `Ctrl+C` in the terminal to stop the server.

## Add books to the catalog

1. Open http://127.0.0.1:8000/admin/ and sign in with the superuser created above.
2. Add an **Author** first.
3. Add a **Book** and select that author. Fill in title, ISBN, publication year, total copies, and available copies. Keep available copies at or below total copies.
4. Visit the catalog page to see the book. Create a normal account from **Create account** to test borrowing and returns.

## Main features

- Search by book title, author, or ISBN; filter to currently available books.
- View book details and an author's profile.
- Register and log in with Django's built-in authentication.
- Borrow available books for 1–30 days.
- Prevent a user from borrowing the same book again while an earlier borrowing is active or overdue.
- Return books and restore the available-copy count.
- View current borrowings, borrowing history, and overdue fine estimates.
- Add/manage authors, books, and borrowing records in Django admin.

## Notes before deployment

These settings are intended for local development (`DEBUG = True`, an example `SECRET_KEY`, and an empty `ALLOWED_HOSTS`). Do not deploy this configuration publicly as-is. Set a private secret key, disable debug mode, configure allowed hosts, and use production-ready static-file and database settings before deployment.
