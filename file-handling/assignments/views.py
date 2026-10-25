from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AssignmentForm
from .models import Assignment


def assignment_list(request):
    """Read: show every saved submission, newest first."""
    assignments = Assignment.objects.all()
    return render(request, "assignments/list.html", {"assignments": assignments})


def upload_assignment(request):
    """Create: receive form fields and the uploaded file, validate, then save."""
    if request.method == "POST":
        # request.FILES is required to receive the actual uploaded file bytes.
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your assignment was uploaded successfully.")
            return redirect("assignments:list")
        messages.error(request, "Please correct the errors below and try again.")
    else:
        form = AssignmentForm()

    return render(request, "assignments/upload.html", {"form": form})
