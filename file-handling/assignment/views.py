from django.shortcuts import redirect, render
from .forms import AssignmentForm
from .models import Assignment


def upload_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("list")
    else:
        form = AssignmentForm()

    return render(request, "upload.html", {"form": form})


def assignment_list(request):
    assignments = Assignment.objects.all().order_by("-submitted_on")
    return render(request, "list.html", {"assignments": assignments})
