from django.contrib import admin
from django.urls import path
from employees import views
urlpatterns = [
 path("admin/",admin.site.urls),
 path("",views.dashboard,name="dashboard"),
 path("login/",views.login_view,name="login"),
 path("logout/",views.logout_view,name="logout"),
 path("departments/",views.department_list,name="department_list"),
 path("departments/add/",views.department_add,name="department_add"),
 path("departments/<int:pk>/edit/",views.department_edit,name="department_edit"),
 path("employees/",views.employee_list,name="employee_list"),
 path("employees/add/",views.employee_add,name="employee_add"),
 path("employees/<int:pk>/edit/",views.employee_edit,name="employee_edit"),
 path("employees/<int:pk>/delete/",views.employee_delete,name="employee_delete"),
 path("attendance/",views.attendance_list,name="attendance_list"),
 path("attendance/add/",views.attendance_add,name="attendance_add"),
 path("leaves/",views.leave_list,name="leave_list"),
 path("leaves/apply/",views.leave_apply,name="leave_apply"),
 path("leaves/<int:pk>/review/",views.leave_review,name="leave_review"),
 path("profile/",views.profile,name="profile"),
]
