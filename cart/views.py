from django.shortcuts import render,get_object_or_404,redirect

from django.contrib import messages


from django.views.generic import ListView , DetailView ,View
from django.views.generic.edit import CreateView, DeleteView, UpdateView 

from django.contrib.auth.decorators import login_required
from cart.models import *
from products.models import *
from .forms import *


class CartView(ListView):
    model = Cart

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        Profile.objects.get_or_create(user=self.request.user)
        obj = Cart.objects.filter(buyer=self.request.user.user)
        order = Order.objects.all()
        c = 0
        for i in obj:
            c =  c + i.get_cost()
            print(c)    
        context['order'] = order
        context ['total'] = c
        context['object_list'] = obj
        return context




class addToCartView(CreateView):
    model = Cart

    def get( self, request,pk, *args, **kwargs ):
        Profile.objects.get_or_create(user=self.request.user)
        item = get_object_or_404(Product,pk=pk)
        order_item, created = Cart.objects.get_or_create(
            item=item,
            buyer=request.user.user
        )
        order_qs = Order.objects.filter(client=request.user.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
			# check if the order item is in the order
            if order.orderitems.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("cart:cart-list")
            else:
                order.orderitems.add(order_item)
                messages.info(request, "This item has been added to your cart.")
                return redirect("cart:cart-list")
        else:
            order = Order.objects.create(
                client=request.user.user)
            order.orderitems.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart:cart-list")



class removeCartView(DeleteView):
    model = Cart

    def get( self, request,pk, *args, **kwargs ):
        Profile.objects.get_or_create(user=self.request.user)
        item = get_object_or_404(Product,pk=pk)
        cart_qs = Cart.objects.filter(buyer=request.user.user, item=item)
        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                cart_qs.delete()
        order_qs = Order.objects.filter(client=request.user.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item__pk=item.pk).exists():
                order_item = Cart.objects.filter(
                    item=item,
                    buyer=request.user.user,
                    )[0]
                order.orderitems.remove(order_item)
                messages.info(request,"This item was removed from your cart.")
                return redirect("cart:cart-list")
            else:
                messages.info(request, "This item has been removed from your cart")
                return redirect("cart:cart-list")
        else:
            messages.info(request, "You do not have an active order")
            return redirect("cart:cart-list")
        return redirect("cart:cart-list")

class CheckOutView(CreateView):
    model = Order
    form_class = CheckOutForm
    template_name = 'cart/checkout_form.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        user = self.request.user.user
        form.fields['orderitems'].queryset = Cart.objects.filter(buyer=user)
        return form

    # def get(self,request,*args,**kwargs):
    #     form = self.form_class(instance=self.request.user.user)
    #     user = self.request.user.user
    #     form.fields['orderitems'].queryset = Cart.objects.filter(buyer=user)

        
    #     context = {
    #         "form": form, 
    #     }
    #     return render(request,self.template_name, context)

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        user = self.request.user.user
        form.fields['orderitems'].queryset = Cart.objects.filter(buyer=user)

        if form.is_valid():
            cart = Cart.objects.filter(buyer= self.request.user.user)
            instance = form.save(commit=False)
            instance.ordered = True
            instance.client_id = request.user.user.id
            instance.save()
            form.save_m2m()
            request.session['order_id'] = instance.pk
            return redirect("payment:process")
        return render(request,self.template_name,{'form':form})#,'forms' : forms})

