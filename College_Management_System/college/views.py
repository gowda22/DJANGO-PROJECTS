from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Department, Course, Student, Faculty, Attendance
from .forms import DepartmentForm, CourseForm, StudentForm, FacultyForm, AttendanceForm

def dashboard(request):
    context = {
        "student_count": Student.objects.count(),
        "faculty_count": Faculty.objects.count(),
        "course_count": Course.objects.count(),
        "department_count": Department.objects.count(),
        "recent_students": Student.objects.select_related("course").order_by("-id")[:5],
        "attendance_count": Attendance.objects.count(),
    }
    return render(request, "college/dashboard.html", context)

def listing(request, model, template, title):
    return render(request, template, {"items": model.objects.all(), "page_title": title})

def departments(request): return listing(request, Department, "college/departments.html", "Departments")
def courses(request): return listing(request, Course, "college/courses.html", "Courses")
def students(request): return listing(request, Student, "college/students.html", "Students")
def faculty(request): return listing(request, Faculty, "college/faculty.html", "Faculty")
def attendance(request):
    return render(request, "college/attendance.html", {"items": Attendance.objects.select_related("student").all()})

def create_item(request, form_class, template, title, success_url):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{title} added successfully.")
        return redirect(success_url)
    return render(request, template, {"form": form, "page_title": f"Add {title}"})

def edit_item(request, model, form_class, pk, template, title, success_url):
    obj = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{title} updated successfully.")
        return redirect(success_url)
    return render(request, template, {"form": form, "page_title": f"Edit {title}"})

def delete_item(request, model, pk, title, success_url):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{title} deleted.")
        return redirect(success_url)
    return render(request, "college/confirm_delete.html", {"object": obj, "page_title": f"Delete {title}"})

def department_add(request): return create_item(request, DepartmentForm, "college/form.html", "Department", "departments")
def department_edit(request, pk): return edit_item(request, Department, DepartmentForm, pk, "college/form.html", "Department", "departments")
def department_delete(request, pk): return delete_item(request, Department, pk, "Department", "departments")
def course_add(request): return create_item(request, CourseForm, "college/form.html", "Course", "courses")
def course_edit(request, pk): return edit_item(request, Course, CourseForm, pk, "college/form.html", "Course", "courses")
def course_delete(request, pk): return delete_item(request, Course, pk, "Course", "courses")
def student_add(request): return create_item(request, StudentForm, "college/form.html", "Student", "students")
def student_edit(request, pk): return edit_item(request, Student, StudentForm, pk, "college/form.html", "Student", "students")
def student_delete(request, pk): return delete_item(request, Student, pk, "Student", "students")
def faculty_add(request): return create_item(request, FacultyForm, "college/form.html", "Faculty", "faculty")
def faculty_edit(request, pk): return edit_item(request, Faculty, FacultyForm, pk, "college/form.html", "Faculty", "faculty")
def faculty_delete(request, pk): return delete_item(request, Faculty, pk, "Faculty", "faculty")
def attendance_add(request): return create_item(request, AttendanceForm, "college/form.html", "Attendance", "attendance")
def attendance_delete(request, pk): return delete_item(request, Attendance, pk, "Attendance", "attendance")
