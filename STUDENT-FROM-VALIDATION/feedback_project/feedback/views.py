from django.shortcuts import render, redirect
from .forms import FeedBackForm
from .models import FeedBack


def feedback_view(request):
    if request.method == 'POST':
        form = FeedBackForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = FeedBackForm()

    return render(request, 'feedback/form.html', {'form': form})


def success_view(request):
    return render(request, 'feedback/success.html')


def display_feedback(request):
    data = FeedBack.objects.all()
    return render(request, 'feedback/display.html', {'data': data})