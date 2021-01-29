from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class CheckOutForm(forms.ModelForm):
	# orderitems = forms.ModelMultipleChoiceField(
 #             queryset=Cart.objects.all(),
 #             widget=forms.CheckboxSelectMultiple,
 #             required=True)
	

	class Meta:
		model = Order
		fields = (
			'orderitems',
			'email',
			'address',
			'city',
			'state',
			'zip_code',
			)


		widgets = {
            'orderitems': forms.CheckboxSelectMultiple,
        }
		# self.fields['orderitems'] = Cart.objects.filter(orderitems__buyer__user=request.user)

	# def __init__(self,user=None,*args, **kwargs):
	#  	 super(CheckOutForm,self).__init__(*args,**kwargs)
	#  	 self.fields['orderitems'].queryset = Cart.objects.filter(buyer=user)