from django.db import models
from django.urls import reverse

from acc.models import * 
from .managers import *

class Category(models.Model):
	caover			= models.ImageField(upload_to="category/cover/",default="category.png")
	more  			= models.TextField(verbose_name="category description",default=None)
	title 			= models.CharField(max_length=700)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	slug			= models.SlugField(default=None)

	def __str__(self):
		return f'{self.title}'

	def snippet(self):
		return self.more[:47] + '...'

class Product(models.Model):
	"""products table"""
	thumb			= models.ImageField(upload_to="products/thum/",default="products.png")
	name 			= models.CharField(max_length=900)
	info 			= models.TextField(verbose_name="product description")
	location		= models.CharField(max_length=10000,default=None)
	price 			= models.IntegerField(default=0.0)
	discount 		= models.IntegerField(default=0.0) 
	timestamp 		= models.DateTimeField(auto_now_add=True)
	is_pub			= models.BooleanField(default=False,verbose_name="published")
	favourite 		= models.ManyToManyField(Profile, related_name='favourite', blank=True,default=None)
	author			= models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="author",default=None)
	category 		= models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category",default=None)
	slug			= models.SlugField(default=None)

	class Meta:
		ordering = ['-timestamp']


	def current_price(self):
		if self.price == 0 and self.discount == 0:
			return f'free'
		elif self.price >= 1 and self.discount >= 1:
			qs = self.price - self.discount
			if qs >= 1:
				return qs
			else:
				return None
		else:
			return None
		

	def get_price(self):

		if self.price >= 1:
			return self.price
		else:
			return None

	def get_absolute_url(self):
		return reverse('products:products-details', args=[self.slug,self.pk])

	def add_to_cart(self):
		return reverse('cart:cart-add', args=[self.pk])

	def get_404(self):
		return reverse('products:oops', args=[self.pk])

	def hundle_wishlist(self):
		return reverse('products:wishlist', args=[self.pk])

	def __str__(self):
		return self.name[:480] 


class moreImgDetails(models.Model):
	product 		= models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product",blank=None)
	img1			= models.ImageField(upload_to="products/thum/",blank=True,verbose_name="first image")
	img2			= models.ImageField(upload_to="products/thum/",blank=True,verbose_name="second image")
	img3			= models.ImageField(upload_to="products/thum/",blank=True,verbose_name="third image")
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects = MoreImgManager()
	def __str__(self):
		return f'more images for {self.product}'




