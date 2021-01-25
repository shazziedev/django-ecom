from django.db import models
from django.contrib.auth.models import User






class Profile(models.Model):
	user 			=	 models.OneToOneField(User, on_delete=models.CASCADE , related_name = 'user')
	avatar 			=	 models.ImageField(upload_to = 'profile/avatar/', default	= 'avatar.jpg',verbose_name="Avatar")	 	
	dob				=	 models.DateField(null=True, blank=True,verbose_name="Date Of Birth",help_text="fomart: 1964-12-31")
	bio 			=	 models.TextField(verbose_name="About Me")
	city			=	 models.CharField(max_length=100)
	zipcode			= 	 models.CharField(max_length=5,blank=True,default=10101)
	street 			= 	 models.CharField(max_length=700,verbose_name="street address",blank=True)
	houseNo			=	 models.CharField(max_length=700,verbose_name="house number",blank=True)
	cell			=	 models.CharField(max_length=12)
	facebook		=	 models.URLField(default="https://",help_text="https://web.facebook.com/kevin")
	instagram		= 	 models.URLField(default="https://",help_text="https://www.instagram.com/kevin")
	email_confirmed = 	 models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user}'
