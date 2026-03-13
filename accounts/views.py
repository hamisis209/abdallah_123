from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.shortcuts import redirect, render


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register_user.html', {'form': form})


def register_guest_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guest registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register_guest.html', {'form': form})


def recover_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request, use_https=request.is_secure(),
                      email_template_name='password_reset_email.html')
            messages.success(request, 'Password reset instructions sent to your email.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/recover_password.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('login')

