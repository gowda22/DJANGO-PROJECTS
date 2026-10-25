from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import FeedbackForm, RegisterForm, StudentUpdateForm
from .models import Feedback, Student


def register(request):
    if request.user.is_authenticated:
        return redirect("student_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("student_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def student_list(request):
    # Authorization/data filtering: staff can view all profiles; a student sees only their own.
    if request.user.is_staff:
        students = Student.objects.select_related("user").all()
    else:
        students = Student.objects.filter(user=request.user)

    return render(request, "students/student_list.html", {"students": students})


def get_student_if_allowed(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # Authentication is enforced by @login_required; this is the per-record authorization check.
    if not request.user.is_staff and student.user_id != request.user.id:
        raise PermissionDenied("You may only manage your own student profile.")
    return student


@login_required
def student_update(request, pk):
    student = get_student_if_allowed(request, pk)

    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            # Keep the account email in sync with the profile email.
            student.user.email = student.email
            student.user.save(update_fields=["email"])
            return redirect("student_list")
    else:
        form = StudentUpdateForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {"form": form, "student": student},
    )


@login_required
@require_POST
def student_delete(request, pk):
    student = get_student_if_allowed(request, pk)
    student.delete()
    # This removes the Student profile only; the Django login account remains.
    return redirect("student_list")


@login_required
def feedback_list(request):
    if request.user.is_staff:
        feedback_items = Feedback.objects.select_related("user").all()
    else:
        feedback_items = Feedback.objects.filter(user=request.user)
    return render(
        request,
        "students/feedback_list.html",
        {"feedback_items": feedback_items},
    )


@login_required
def feedback_create(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # Never trust a submitted user ID. The logged-in user owns this feedback.
            feedback.user = request.user
            feedback.save()
            return redirect("feedback_list")
    else:
        form = FeedbackForm()
    return render(request, "students/feedback_form.html", {"form": form})


@login_required
@require_POST
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if not request.user.is_staff and feedback.user_id != request.user.id:
        raise PermissionDenied("You may only delete your own feedback.")
    feedback.delete()
    return redirect("feedback_list")
