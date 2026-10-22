from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Feedback
from .forms import FeedbackForm
from accounts.decorators import role_required


# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# Student submits feedback
@login_required
@role_required('student')
def submit_feedback(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('dashboard')

    else:
        form = FeedbackForm()

    return render(request, 'submit.html', {'form': form})


# Admin views all feedback
@login_required
@role_required('admin')
def view_feedback(request):

    data = Feedback.objects.select_related('user').all()

    return render(request, 'view.html', {'data': data})