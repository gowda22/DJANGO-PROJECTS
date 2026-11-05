from django.conf import settings
from django.db import models

class Department(models.Model):
 name=models.CharField(max_length=100,unique=True)
 description=models.CharField(max_length=250,blank=True)
 def __str__(self): return self.name

class Employee(models.Model):
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="employee_profile")
 employee_id=models.CharField(max_length=20,unique=True)
 department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
 designation=models.CharField(max_length=100,blank=True)
 phone=models.CharField(max_length=20,blank=True)
 joining_date=models.DateField(null=True,blank=True)
 salary=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 address=models.TextField(blank=True)
 def __str__(self): return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

class Attendance(models.Model):
 STATUS=[("Present","Present"),("Absent","Absent"),("Late","Late"),("Half Day","Half Day")]
 employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="attendance")
 date=models.DateField()
 status=models.CharField(max_length=20,choices=STATUS,default="Present")
 check_in=models.TimeField(null=True,blank=True)
 check_out=models.TimeField(null=True,blank=True)
 notes=models.CharField(max_length=250,blank=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=["employee","date"],name="unique_employee_attendance_day")]
  ordering=["-date","employee__employee_id"]
 def __str__(self): return f"{self.employee} - {self.date}"

class LeaveRequest(models.Model):
 TYPES=[("Casual","Casual"),("Sick","Sick"),("Earned","Earned"),("Other","Other")]
 STATUS=[("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")]
 employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="leave_requests")
 leave_type=models.CharField(max_length=20,choices=TYPES)
 start_date=models.DateField()
 end_date=models.DateField()
 reason=models.TextField()
 status=models.CharField(max_length=20,choices=STATUS,default="Pending")
 reviewed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="reviewed_leaves")
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=["-created_at"]
 def __str__(self): return f"{self.employee} - {self.leave_type} ({self.status})"
