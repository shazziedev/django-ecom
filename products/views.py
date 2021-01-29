from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView ,View
from django.views.generic.edit import CreateView, DeleteView, UpdateView 

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *
from .forms import *


class productList(ListView):
	model = Product
	paginate_by = 4
	
	
	def get_context_data(self,*args, **kwargs):
		
		context = super().get_context_data(**kwargs)
		cat = Category.objects.all()
		context['cat'] = cat
		# context['is_favourite'] = is_favourite
		return context

class productDetails(DetailView):
	model = Product
	template_name = 'products/products-detail.html' 
	

	def get( self, request,pk, *args, **kwargs ):
		 is_favourite = False
		 pro = get_object_or_404(Product,pk=pk)
		 if pro.favourite.filter(id=request.user.user.id).exists():
			 is_favourite = True
		 try:
			 self.object = self.get_object()
		 except Http404:
			 # redirect here
			 return redirect("products:oops")

		 context = self.get_context_data(object=self.object,is_favourite=is_favourite)
		 return self.render_to_response(context)
			

class addProductView(CreateView,LoginRequiredMixin):
	model 			= Product
	form_class 		= ProductForm
	custom_form		= MoreImgProductForm 
	template_name 	= 'products/product_form.html'

	def get(self, request, *args, **kwargs ):
		form = self.form_class()
		forms = self.custom_form()
		context = {
			"form": form,
			'forms':forms,
		}
		return render(request,self.template_name,context)

	def post(self, request, *args, **kwargs ):
		form = self.form_class(request.POST,request.FILES)
		forms = self.custom_form(request.FILES,request.POST)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user.user
			instance.save()
			more_form = forms.save(False)
			more_form.product = instance
			more_form.save()
			return redirect("products:products-list")
		return render(request,self.template_name,{'form':form})#,'forms' : forms})

class productOops(View):
	model = Product
	template_name = 'products/oops.html'

	def get( self, request, *args, **kwargs ):
		return render(request,self.template_name)
		




class WishList(DetailView):
	model = Product

	def get( self, request,pk, *args, **kwargs ):
		Profile.objects.get_or_create(user=self.request.user)
		product = get_object_or_404(Product,pk=pk)
		if product.favourite.filter(id=self.request.user.user.id).exists():
			product.favourite.remove(request.user.user)
		else:
			product.favourite.add(request.user.user)
		return redirect(product.get_absolute_url())


    
class WishListView(ListView):
	model = Product

	def get(self, request,*args, **kwargs):
		me = request.user.user
		wishlist = me.favourite.all()
		context = {
		'wishlist' : wishlist
		}
		return render(request, 'products/wish_list.html', context)
