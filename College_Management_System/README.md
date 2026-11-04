# College Management System (Django)

A beginner-friendly college management project with a clean, simple UI.

## Features
- Dashboard summary
- Department management
- Course management
- Student management
- Faculty management
- Attendance records
- Django admin
- SQLite database (no separate database setup)

## Setup (Windows PowerShell)
1. Extract the ZIP.
2. Open the extracted `College_Management_System` folder in VS Code.
3. Open terminal in the folder containing `manage.py`.
4. Create virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Create database tables:
   ```powershell
   python manage.py makemigrations college
   python manage.py migrate
   ```
7. Create admin:
   ```powershell
   python manage.py createsuperuser
   ```
8. Run:
   ```powershell
   python manage.py runserver
   ```
9. Open http://127.0.0.1:8000/ . Admin: http://127.0.0.1:8000/admin/

## GitHub
```powershell
git init
git add .
git commit -m "Initial college management system"
```
Create an empty GitHub repository, then:
```powershell
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/college-management-system.git
git push -u origin main
```
Replace the URL with your own repository URL. Do not upload `.venv` or secret files.

## Project structure
- `college_project/settings.py`: project configuration
- `college/ models.py`: database tables
- `college/views.py`: page behavior
- `college/urls.py`: app routes
- `college/forms.py`: forms and validation
- `college/templates/`: HTML
- `college/static/college/style.css`: external CSS

This is a learning project. Add sample data through the website or Django admin.
