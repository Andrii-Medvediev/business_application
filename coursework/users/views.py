from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, CustomAuthenticationForm, ProfileForm

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація пройшла успішно!')
            return redirect('finance:accounts')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/sign_up.html', {'form': form})

def log_in(request):
    error_message = None
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('finance:accounts')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/log_in.html', {'form': form})


@login_required
def view_profile(request):
    profile = request.user.profile
    return render(request, 'users/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлено.')
            return redirect('users:view_profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})

@login_required
def logout_user(request):
    logout(request)
    return redirect('users:log_in')