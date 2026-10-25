# Django File Handling — Assignment Upload Project

This project follows the code and flow in your uploaded reference photos. It is intentionally kept small so you can study each file in order. It includes only assignment file upload/listing, not student accounts or authentication.

## Project structure

```text
assignment_project_file_handling/
├── manage.py
├── requirements.txt
├── db.sqlite3                 # created after migrate
├── media/                     # uploaded files are stored here
│   └── assignments/           # created when the first file is uploaded
├── assignment/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   ├── upload.html
│   │   └── list.html
│   └── static/
│       └── assignment/
│           └── style.css
└── assignment_project/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

## Set up on Windows PowerShell

Open this extracted folder in VS Code. Open the terminal in the folder that contains `manage.py`.

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open these pages:

- Upload page: http://127.0.0.1:8000/
- Uploaded assignment list: http://127.0.0.1:8000/list/
- Admin (optional): http://127.0.0.1:8000/admin/

To use Django admin, create an admin account first:

```powershell
python manage.py createsuperuser
```

## What each file does

1. `models.py` — describes the database record: student name, course, file and submission date.
2. `forms.py` — `ModelForm` creates a form from the `Assignment` model.
3. `views.py` — handles GET (show empty form), POST (receive and save the upload), and listing records.
4. `assignment/urls.py` — maps `/` to upload and `/list/` to the list.
5. `assignment_project/urls.py` — connects app URLs and serves uploaded media during local development.
6. `settings.py` — registers the app and configures SQLite, static CSS and uploaded media.
7. `upload.html` — contains `method="POST"`, `{% csrf_token %}`, and `enctype="multipart/form-data"`.
8. `list.html` — loops through assignments and shows a download link.
9. `style.css` — a small set of straightforward styling rules only; it does not change the upload logic.

## How file upload works

Browser form → app URL → `upload_assignment()` view → `AssignmentForm(request.POST, request.FILES)` → `form.is_valid()` → `form.save()` → database record plus file under `media/assignments/` → redirect to `/list/`.

`request.POST` carries normal text fields. `request.FILES` carries uploaded file data. The HTML form needs `enctype="multipart/form-data"` so the browser sends the file correctly.

## Important notes

- `MEDIA_ROOT` is the local folder where uploaded files are saved; `MEDIA_URL` is the URL prefix used to access them in development.
- Django's `static()` helper in the project URL configuration serves media only while `DEBUG=True`; it is for local development, not production.
- `fields = "__all__"` follows the reference code. The `submitted_on` field is automatically set by Django and is not editable in the form.
- This teaching example does not impose file-size/type restrictions or authentication because those are not shown in the uploaded reference code. Add these deliberately as separate next steps when you understand the base project.
