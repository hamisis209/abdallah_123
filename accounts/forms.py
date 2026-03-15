from django import forms
from django.contrib.auth.models import User

from .models import Profile


class ProfileForm(forms.ModelForm):
	username = forms.CharField(max_length=150)
	email = forms.EmailField(required=False)
	first_name = forms.CharField(max_length=150, required=False)
	last_name = forms.CharField(max_length=150, required=False)

	class Meta:
		model = Profile
		fields = [
			'username',
			'email',
			'first_name',
			'last_name',
			'photo',
			'student_id',
			'gender',
			'program',
			'phone_number',
			'address',
			'city',
			'country',
			'emergency_contact_name',
			'emergency_contact_phone',
			'disability_status',
			'disability_description',
			'assistive_devices',
		]

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		self.fields['phone_number'].label = 'Phone'
		if self.user:
			self.fields['username'].initial = self.user.username
			self.fields['email'].initial = self.user.email
			self.fields['first_name'].initial = self.user.first_name
			self.fields['last_name'].initial = self.user.last_name

	def clean_username(self):
		username = self.cleaned_data['username']
		user = self.user or self.instance.user
		if User.objects.filter(username=username).exclude(pk=user.pk).exists():
			raise forms.ValidationError('This username is already taken.')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email', '').strip()
		user = self.user or self.instance.user
		if email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
			raise forms.ValidationError('This email is already in use.')
		return email

	def save(self, commit=True):
		profile = super().save(commit=False)
		user = self.user or profile.user
		user.username = self.cleaned_data['username']
		user.email = self.cleaned_data.get('email', '')
		user.first_name = self.cleaned_data.get('first_name', '')
		user.last_name = self.cleaned_data.get('last_name', '')
		if commit:
			user.save()
			profile.user = user
			profile.save()
		return profile
