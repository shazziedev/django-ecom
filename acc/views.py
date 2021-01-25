from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,  redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required 
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login , logout
from django.views.generic import View, UpdateView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from . models import Profile
from . form_user import (EditProfileForm, ProfileForm)
from . signup_form import SignUpForm
from . import form_user
from . tokens import account_activation_token

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class UserView(View):
	model = Profile
	template_name = 'acc/user_index.html'
	
	def get(self,request,*args,**kwargs):
         Profile.objects.get_or_create(user=self.request.user)
         obj = Profile.objects.filter(user=request.user)
         context = {'obj' : obj}
         return render(request,self.template_name,context)
        
    
    
class EditProfile(View):
    model                    = Profile
    form_class               = EditProfileForm    
    custom_form_classes      = ProfileForm
    template_name            = 'acc/edit_form.html'

    def get(self, request, *args, **kwargs):
        Profile.objects.get_or_create(user=self.request.user)
        form = self.form_class(instance=self.request.user)
        me = self.request.user
        if Profile.objects.filter(user=me).exists():
            custom_form  = self.custom_form_classes(instance=self.request.user.user)
        else:
            custom_form  = self.custom_form_classes()
        context = {
        'form':form,
        'custom_form': custom_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        me = self.request.user
        if Profile.objects.filter(user=me).exists():
            custom_form = ProfileForm(request.POST, request.FILES,instance=self.request.user.user)
        else:
            custom_form = ProfileForm(request.POST, request.FILES)
        form = EditProfileForm(request.POST,instance=self.request.user)
        if form.is_valid() and custom_form.is_valid():
            django_form = form.save()
            custom_django_form = custom_form.save(False)
            custom_django_form.user = django_form
            custom_django_form.save()
            messages.success(request, ('Profile Updated successfully.'))
            return redirect('acc:index')

        return render(request, self.template_name, {'form' : form , 'custom_form' : custom_form})
    
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            #create_custom_user_profile
            Profile.objects.get_or_create(user=user)

            current_site = get_current_site(request)
            site = current_site.domain
            subject = 'Activate Your %(site) Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.We have sent a confirmation link to your email. '))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            Profile.user.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your email has been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')



def DeactivateView(request):
    user = request.user
    user.is_active = False
    user.save()
    messages.success(request, ('Profile successfully disabled.'))
    return redirect('acc:index')

def DeleteAccView(request):
    user = request.user
    user.is_active = False
    user.delete()
    messages.success(request, ('Profile successfully deleted.'))
    return redirect('acc:index')




    

