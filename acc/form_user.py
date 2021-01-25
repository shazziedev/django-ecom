from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import Profile

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ('avatar',
			'dob',
			'bio', 
			'city', 
			'bio',
			'cell',
			'facebook',
			'instagram'
			) 
	
class EditProfileForm(ModelForm):
	class Meta:
		model = User
		fields = (
			'email',
			'first_name',
			'last_name',
			)



