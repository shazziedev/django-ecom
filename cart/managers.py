from django.db import models
from django.db.models import Avg
from products.models import *
from acc.models import *
import uuid

from .utils import unique_order_id_generator
from django.db.models.signals import pre_save


class cartManager(models.Manager):
	def get_costf(self):
		pr = getattr(self.item,'current_price')
		if  pr and self.quantity >= 1:
			qs = pr() * self.quantity
		return qs

	def get_total(self, quantity, price):
		if quantity >= 1 and price >=1:
			total = quantity * price
		return total 

	def get_total_price(self,cart_price,shipping_fee):
		return sum([cart_price,shipping_fee])


class OrderManager(models.Manager):
	pass
