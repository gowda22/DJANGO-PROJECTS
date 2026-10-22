from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import RigisterForm


# Registration view
def rigister_view(request):

    if request.method == 'POST':
        form = RigisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('dashboard')

    else:
        form = RigisterForm()

    return render(request, 'register.html', {'form': form})


# Login view
def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('dashboard')

    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):

    logout(request)

    return redirect('login')