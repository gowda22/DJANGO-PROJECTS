from django import forms
from django.contrib.auth.models import User, Group
from django.db import transaction
from .models import Department, Employee, Attendance, LeaveRequest

class DepartmentForm(forms.ModelForm):
 class Meta:
  model=Department
  fields=["name","description"]

class EmployeeForm(forms.ModelForm):
 first_name=forms.CharField(max_length=150)
 last_name=forms.CharField(max_length=150,required=False)
 username=forms.CharField(max_length=150)
 email=forms.EmailField(required=False)
 password=forms.CharField(widget=forms.PasswordInput,required=False,help_text="Required for a new employee account.")
 class Meta:
  model=Employee
  fields=["employee_id","department","designation","phone","joining_date","salary","address"]
 def __init__(self,*args,**kwargs):
  self.user_instance=kwargs.get("instance").user if kwargs.get("instance") else None
  super().__init__(*args,**kwargs)
  if self.user_instance:
   self.fields["first_name"].initial=self.user_instance.first_name
   self.fields["last_name"].initial=self.user_instance.last_name
   self.fields["username"].initial=self.user_instance.username
   self.fields["email"].initial=self.user_instance.email
   self.fields["password"].required=False
 def clean_username(self):
  username=self.cleaned_data["username"]
  qs=User.objects.filter(username=username)
  if self.user_instance: qs=qs.exclude(pk=self.user_instance.pk)
  if qs.exists(): raise forms.ValidationError("This username already exists.")
  return username
 def clean(self):
  cleaned=super().clean()
  if not self.user_instance and not cleaned.get("password"):
   self.add_error("password","Password is required for a new user.")
  return cleaned
 @transaction.atomic
 def save(self,commit=True):
  employee=super().save(commit=False)
  if self.user_instance:
   user=self.user_instance
  else:
   user=User()
  user.username=self.cleaned_data["username"]
  user.first_name=self.cleaned_data["first_name"]
  user.last_name=self.cleaned_data.get("last_name","")
  user.email=self.cleaned_data.get("email","")
  if self.cleaned_data.get("password"): user.set_password(self.cleaned_data["password"])
  if commit:
   user.save()
   employee.user=user
   employee.save()
   employee.groups_dummy=None if False else None
   group,created=Group.objects.get_or_create(name="Employee")
   user.groups.add(group)
   self.save_m2m()
  else:
   employee.user=user
  return employee

class AttendanceForm(forms.ModelForm):
 class Meta:
  model=Attendance
  fields=["employee","date","status","check_in","check_out","notes"]
  widgets={"date":forms.DateInput(attrs={"type":"date"}),"check_in":forms.TimeInput(attrs={"type":"time"}),"check_out":forms.TimeInput(attrs={"type":"time"})}

class LeaveForm(forms.ModelForm):
 class Meta:
  model=LeaveRequest
  fields=["leave_type","start_date","end_date","reason"]
  widgets={"start_date":forms.DateInput(attrs={"type":"date"}),"end_date":forms.DateInput(attrs={"type":"date"})}
 def clean(self):
  data=super().clean()
  start,end=data.get("start_date"),data.get("end_date")
  if start and end and end<start: self.add_error("end_date","End date must be on or after start date.")
  return data
