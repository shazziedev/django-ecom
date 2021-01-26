from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from products.views import productList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('cart/',include('cart.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('products/',include('products.urls')),
    path('accounts/',include('acc.urls')),
    path('payment/',include('payment.urls')),	
    path('auth/',include('django.contrib.auth.urls')),
    path('oauth/',include('social_django.urls',namespace="social")),
	path('',productList.as_view(template_name="home.html"),name='home'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
