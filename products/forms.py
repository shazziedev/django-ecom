from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import *

class ProductForm(ModelForm):
	# image_one = forms.ImageField( required=False, help_text='Additional image. Optional')
	# image_two = forms.ImageField( required=False, help_text='Additional image. Optional')
	# image_three = forms.ImageField( required=False, help_text='Additional image. Optional')

	class Meta:
		model = Product
		fields = (
			'thumb',
			'name',
			'info', 
			'location', 
			'price', 
			'discount',
			'category',
			'slug',
			# 'image_one',
			# 'image_two',
			# 'image_three', 
			 ) 

class MoreImgProductForm(ModelForm):
	class Meta:
		model = moreImgDetails
		fields = (
			'img1',
			'img2',
			'img3',
			) 