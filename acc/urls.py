from django.conf.urls import url
from django.urls import path
from .views import *

from django.contrib.auth.decorators import login_required

app_name = 'acc'

urlpatterns = [
	path('', login_required(UserView.as_view()),name='index'),
    path('signup/', SignUpView.as_view(template_name = 'registration/signup.html'), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('profile/edit/', login_required(EditProfile.as_view()) , name ='edit'),
    path('update/', login_required(UpdateView.as_view()), name="update"),
 	path('deactivate/', DeactivateView , name ='deactivate'),
    path('so-long/',DeleteAccView,name='delete'),
    path('notification/',Notice,name='notice'),

]
