from django import forms
from .models import Department, Course, Student, Faculty, Attendance

class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class DepartmentForm(StyledModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        fields = ["name", "course_code", "department", "duration_years"]

class StudentForm(StyledModelForm):
    class Meta:
        model = Student
        fields = ["enrollment_no", "full_name", "email", "phone", "course", "semester"]

class FacultyForm(StyledModelForm):
    class Meta:
        model = Faculty
        fields = ["faculty_id", "full_name", "email", "department", "designation"]

class AttendanceForm(StyledModelForm):
    class Meta:
        model = Attendance
        fields = ["student", "date", "subject", "status"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
