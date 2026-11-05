# WorkTrack HR Management System (Empty starter)

This project has **no demo users, no demo employees, no demo attendance, and no demo leave requests**.
You will create the Admin account yourself and add HR/Employee users and data through the application.

## Windows PowerShell setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations employees
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ and sign in with the superuser you created.
Django Admin: http://127.0.0.1:8000/admin/

## Roles
- **Admin:** Django superuser. Create HR and Employee accounts yourself.
- **HR:** Add/manage employees, departments, attendance, and review leave.
- **Employee:** View own profile/attendance/leave and submit leave requests.

No sample data or pre-created credentials are included.






WORKFLOW CHART OF ALL IN OUR PROJECT