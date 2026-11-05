from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from .models import Department,Employee,Attendance,LeaveRequest
from .forms import DepartmentForm,EmployeeForm,AttendanceForm,LeaveForm

def role(user):
 if not user.is_authenticated: return "Guest"
 if user.is_superuser: return "Admin"
 names=set(user.groups.values_list("name",flat=True))
 for r in ("Admin","HR","Employee"):
  if r in names: return r
 return "Employee"

def roles_required(*allowed):
 def decorator(view):
  @login_required
  @wraps(view)
  def wrapped(request,*args,**kwargs):
   if role(request.user) not in allowed:
    messages.error(request,"You do not have permission to access that page.")
    return redirect("dashboard")
   return view(request,*args,**kwargs)
  return wrapped
 return decorator

def login_view(request):
 if request.user.is_authenticated: return redirect("dashboard")
 if request.method=="POST":
  user=authenticate(request,username=request.POST.get("username",""),password=request.POST.get("password",""))
  if user:
   login(request,user); return redirect("dashboard")
  messages.error(request,"Invalid username or password.")
 return render(request,"registration/login.html")

@login_required
def logout_view(request):
 logout(request); return redirect("login")

@login_required
def dashboard(request):
 r=role(request.user)
 context={"role":r,"employee_count":Employee.objects.count(),"department_count":Department.objects.count(),
  "today_attendance":Attendance.objects.filter(date__year=__import__("datetime").date.today().year,date__month=__import__("datetime").date.today().month,date__day=__import__("datetime").date.today().day).count(),
  "pending_leaves":LeaveRequest.objects.filter(status="Pending").count()}
 if r=="Employee":
  emp=Employee.objects.filter(user=request.user).first()
  context["employee"]=emp
  context["my_attendance"]=Attendance.objects.filter(employee=emp)[:5] if emp else []
  context["my_leaves"]=LeaveRequest.objects.filter(employee=emp)[:5] if emp else []
 return render(request,"employees/dashboard.html",context)

@roles_required("Admin","HR")
def department_list(request):
 return render(request,"employees/departments.html",{"departments":Department.objects.all()})
@roles_required("Admin","HR")
def department_add(request):
 form=DepartmentForm(request.POST or None)
 if form.is_valid(): form.save(); messages.success(request,"Department created."); return redirect("department_list")
 return render(request,"employees/department_form.html",{"form":form,"title":"Add Department"})
@roles_required("Admin","HR")
def department_edit(request,pk):
 obj=get_object_or_404(Department,pk=pk); form=DepartmentForm(request.POST or None,instance=obj)
 if form.is_valid(): form.save(); messages.success(request,"Department updated."); return redirect("department_list")
 return render(request,"employees/department_form.html",{"form":form,"title":"Edit Department"})

@roles_required("Admin","HR")
def employee_list(request):
 qs=Employee.objects.select_related("user","department")
 q=request.GET.get("q","").strip()
 if q: qs=qs.filter(Q(user__first_name__icontains=q)|Q(user__last_name__icontains=q)|Q(employee_id__icontains=q)|Q(user__username__icontains=q))
 return render(request,"employees/employee_list.html",{"employees":qs,"q":q})
@roles_required("Admin","HR")
def employee_add(request):
 form=EmployeeForm(request.POST or None)
 if form.is_valid(): form.save(); messages.success(request,"Employee account created. Assign HR role from Admin if needed."); return redirect("employee_list")
 return render(request,"employees/employee_form.html",{"form":form,"title":"Add Employee"})
@roles_required("Admin","HR")
def employee_edit(request,pk):
 obj=get_object_or_404(Employee,pk=pk); form=EmployeeForm(request.POST or None,instance=obj)
 if form.is_valid(): form.save(); messages.success(request,"Employee updated."); return redirect("employee_list")
 return render(request,"employees/employee_form.html",{"form":form,"title":"Edit Employee"})
@roles_required("Admin")
def employee_delete(request,pk):
 obj=get_object_or_404(Employee,pk=pk)
 if request.method=="POST": obj.user.delete(); messages.success(request,"Employee deleted."); return redirect("employee_list")
 return render(request,"employees/confirm_delete.html",{"object":obj})

@roles_required("Admin","HR")
def attendance_list(request):
 qs=Attendance.objects.select_related("employee","employee__user")
 q=request.GET.get("q","").strip()
 if q: qs=qs.filter(Q(employee__employee_id__icontains=q)|Q(employee__user__first_name__icontains=q))
 return render(request,"employees/attendance_list.html",{"records":qs,"q":q})
@roles_required("Admin","HR")
def attendance_add(request):
 form=AttendanceForm(request.POST or None)
 if form.is_valid(): form.save(); messages.success(request,"Attendance saved."); return redirect("attendance_list")
 return render(request,"employees/attendance_form.html",{"form":form})

@login_required
def leave_list(request):
 r=role(request.user)
 qs=LeaveRequest.objects.select_related("employee","employee__user")
 if r=="Employee":
  emp=Employee.objects.filter(user=request.user).first()
  qs=qs.filter(employee=emp) if emp else qs.none()
 return render(request,"employees/leaves.html",{"leaves":qs,"role":r})
@roles_required("Employee")
def leave_apply(request):
 emp=get_object_or_404(Employee,user=request.user)
 form=LeaveForm(request.POST or None)
 if form.is_valid():
  leave=form.save(commit=False); leave.employee=emp; leave.save()
  messages.success(request,"Leave request submitted."); return redirect("leave_list")
 return render(request,"employees/leave_form.html",{"form":form})
@roles_required("Admin","HR")
def leave_review(request,pk):
 leave=get_object_or_404(LeaveRequest,pk=pk)
 if request.method=="POST" and leave.status=="Pending":
  status=request.POST.get("status")
  if status in ("Approved","Rejected"):
   leave.status=status; leave.reviewed_by=request.user; leave.save()
   messages.success(request,f"Leave {status.lower()}.")
 return redirect("leave_list")

@login_required
def profile(request):
 emp=Employee.objects.filter(user=request.user).first()
 return render(request,"employees/profile.html",{"employee":emp,"role":role(request.user)})
