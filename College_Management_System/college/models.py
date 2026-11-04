from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=12, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return f"{self.code} - {self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="courses")
    duration_years = models.PositiveSmallIntegerField(default=4)
    def __str__(self): return f"{self.course_code} - {self.name}"

class Student(models.Model):
    enrollment_no = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="students")
    semester = models.PositiveSmallIntegerField(default=1)
    joined_on = models.DateField(auto_now_add=True)
    def __str__(self): return f"{self.enrollment_no} - {self.full_name}"

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="faculty")
    designation = models.CharField(max_length=80, default="Assistant Professor")
    def __str__(self): return f"{self.faculty_id} - {self.full_name}"

class Attendance(models.Model):
    STATUS = [("Present", "Present"), ("Absent", "Absent")]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default="Present")
    subject = models.CharField(max_length=100)
    class Meta:
        ordering = ["-date", "student__full_name"]
        constraints = [models.UniqueConstraint(fields=["student", "date", "subject"], name="unique_student_attendance_subject_date")]
    def __str__(self): return f"{self.student.full_name} - {self.date} - {self.status}"
