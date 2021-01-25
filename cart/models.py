from django.db import models

from products.models import *
from acc.models import *
import uuid

from .utils import unique_order_id_generator
from django.db.models.signals import pre_save


class cartManager(models.Manager):
    def get_total(self, quantity, price):
        if quantity >= 1 and price >=1:
            total = quantity * price
            return total 


class Cart(models.Model):
    buyer 		= models.ForeignKey(Profile, on_delete=models.CASCADE , default=None, related_name="buyer" ) 
    item 		= models.ForeignKey(Product, on_delete=models.CASCADE , default=None, related_name="item" )
    quantity 	= models.IntegerField(default=1)
    created 	= models.DateTimeField(auto_now_add=True)

    objects = cartManager()

    def get_cost(self):
        pr = getattr(self.item,'current_price')
        if  pr and self.quantity >= 1:
             qs = pr() * self.quantity
        return qs


    def remove_from_cart(self):
        return reverse('products:cart-remove', args=[self.item.pk])

     
    def __str__(self):
        return f'{self.quantity} of {self.item.name}'
    


class Order(models.Model):
    ORDER_STATUS_CHOICES= (
    ('Not Yet Shipped', 'Not Yet Shipped'),
    ('Shipped', 'Shipped'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
    )
    orderitems      = models.ManyToManyField(Cart, related_name="orderitems")
    order_id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client 		    = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="client")
    ordered 	    = models.BooleanField(default=False)
    status          = models.CharField(max_length=120, default='Not Yet Shipped', choices= ORDER_STATUS_CHOICES)
    created 	    = models.DateTimeField(auto_now_add=True)
    shipping_fee    = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    
    def __str__(self):
        return f' {self.status}'


    def pre_save_create_order_id(sender, instance, *args, **kwargs):
        if not instance.order_id:
            instance.order_id= unique_order_id_generator(instance)
pre_save.connect(Order.pre_save_create_order_id, sender=Order)
