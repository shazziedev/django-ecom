from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from decimal import Decimal
#from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from  cart.models import Order




@csrf_exempt
def payment_done():
    return render(request,'payment/done.html')




@csrf_exempt
def payment_canceled():
    return render(request,'payment/canceled.html')


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,order_id=order_id)
    host = request.get_host()


    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "%.2f" % order.orderitems.get_cost().quantize(Decimal('0.1')) ,
        "item_name": f'order {order.id}',
        "invoice":str(order.id),
        'currency_code': 'USD',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:canceled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "form": form,
        'order':order,
        }
    return render(request, "payment/process.html", context)