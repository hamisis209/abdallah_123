def transcribe_view(request):
	return render(request, 'transcribe.html')
from django.contrib.auth import logout
def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('login')
def dashboard_view(request):
	return render(request, 'dashboard.html')
def register_guest_view(request):
	# Placeholder: implement guest registration logic as needed
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Guest registration successful. You can now log in.')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'register_guest.html', {'form': form})
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Registration successful. You can now log in.')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'register_user.html', {'form': form})

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
	return render(request, 'recover_password.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.error(request, 'Invalid username or password.')
	return render(request, 'login.html')
