# Django Student Portal — Learning Reference

This is one beginner-friendly example covering models, forms, field validation, CRUD, registration, login/logout, feedback, authentication, authorization, URLs, templates, admin, relationships, and migrations.

## 1. Project layout

```text
project-folder/
├── manage.py
├── requirements.txt
├── student_portal/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── students/
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── templates/
        ├── base.html
        ├── registration/
        │   ├── register.html
        │   └── login.html
        └── students/
            ├── student_list.html
            ├── student_form.html
            ├── feedback_form.html
            └── feedback_list.html
```

## 2. Windows setup

Open PowerShell in the folder containing `manage.py`:

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations students
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open these paths in your browser:

- Register: `http://127.0.0.1:8000/accounts/register/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Student list: `http://127.0.0.1:8000/students/`
- Feedback form: `http://127.0.0.1:8000/students/feedback/add/`
- Feedback list: `http://127.0.0.1:8000/students/feedback/`
- Admin: `http://127.0.0.1:8000/admin/`

A normal student sees only their own profile. Staff users see all profiles. A logged-in user may edit/delete only their own profile unless they are staff. The delete route accepts POST only. Deleting a profile does not delete the Django account.

## 3. What each file answers

- `models.py`: What should be stored in the database?
- `forms.py`: What input should be accepted and validated?
- `views.py`: What should happen for GET and POST requests?
- app `urls.py`: Which URL calls which view?
- project `urls.py`: Which app/auth URLs are connected to the project?
- templates: What should be shown in the browser?
- `settings.py`: Which apps, middleware, templates, database and redirects are configured?
- `admin.py`: How should a model appear in Django admin?

## 4. Validation concepts shown

- Field types: `CharField`, `EmailField`, `ChoiceField`, `IntegerField`, `PositiveSmallIntegerField`.
- Built-in field checks and required fields.
- `max_length`, `unique=True`, `choices`, and field validators.
- `RegexValidator`, `MinValueValidator`, `MaxValueValidator`.
- `clean_name()` and `clean_email()` for field-specific checks.
- `clean()` for a rule that depends on multiple fields (add an actual project rule there when one is required).
- `form.is_valid()`, `form.cleaned_data`, and `forms.ValidationError`.
- A `ModelForm` runs form/model validation for the fields it includes. Calling `model.save()` itself does not automatically call `full_clean()`.

## 5. Authentication vs authorization vs validation

- **Validation:** Is the submitted data acceptable? Example: name characters, age range, email format.
- **Authentication:** Who is this user? Example: Django checks the username/password at login and keeps the user authenticated in the session.
- **Authorization:** Is the authenticated user allowed to do this action? Example: a user can only edit their own profile; staff can manage all profiles.

The built-in Django user model handles account credentials; the `Student` model stores student profile details. Do not add a plain-text password field to your own model.

## 6. Create / Read / Update / Delete (CRUD)

- **Create:** registration form creates a user and student profile; feedback form creates a Feedback record.
- **Read:** `student_list` queries profiles and renders them.
- **Update:** `StudentUpdateForm(instance=student)` pre-fills and updates a profile.
- **Delete:** POST-only views delete a profile or feedback item after the authorization check.

## 7. Relationships and feedback example

- `Student.user` is a `OneToOneField`: one account has one student profile.
- `Feedback.user` is a `ForeignKey`: one account can submit many feedback messages.
- `on_delete=models.CASCADE` means related profile/feedback records are deleted if the user account is deleted.
- Feedback creation uses `form.save(commit=False)` so the view can set `feedback.user = request.user` before saving. Do not accept ownership from a hidden HTML input.

## 8. Request flow to memorize

Browser URL → project `urls.py` → app `urls.py` → view → form validation → model/database → template or redirect → browser.

## 9. Important learning note

This is a study/demo project, not a production deployment configuration. Before deployment, set a secure secret key, turn `DEBUG` off, configure `ALLOWED_HOSTS`, HTTPS/cookie/security settings, and review the full deployment checklist in the Django docs.
