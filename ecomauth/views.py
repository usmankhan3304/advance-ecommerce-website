from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
#activate the user account
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
#import token gerneator
from .utils import *

#for emial 
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
#import threading
import threading

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self) 

    def run(self):
        self.email_message.send()

# Create your views here

def signup(request):
    
    if request.method== "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')

        password1=request.POST.get('password1')
        confir_password=request.POST.get('password2')
        
        if confir_password != password1:
            messages.error(request,"password not matched!")
            return HttpResponseRedirect(request.path_info)
        try:
            user_obj=User.objects.filter(username=email)
            
            if user_obj.exists():
                messages.error(request,"user already exists try another name plzs")
                return HttpResponseRedirect(request.path_info)
        
       
        except Exception as e:
            pass
    

        user_obj=User.objects.create(first_name=first_name,last_name=last_name,username=email,email=email)
        user_obj.set_password(password1)
        user_obj.is_active=False
        user_obj.save()
        # print("the encode id is:",urlsafe_base64_encode(force_bytes(user_obj.pk)))
        current_site=get_current_site(request)
        email_subject="please activate your Account"
        
        message=render_to_string('auths/activate.html',{
            'user':user_obj,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(
            user_obj.pk)),
            'token':generate_token.make_token(user_obj) 
            
        })

        email_from = settings.EMAIL_HOST_USER
        email_message = EmailMessage(email_subject,message,email_from,[email])
        EmailThread(email_message).start()

        messages.info(request,"activate your account by clicking on your received email " )
        return redirect('/ecomauth/login')
            
            
    return render(request,'auths/signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as e:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"account activated succssfully")
            return redirect('/ecomauth/login')
        return render(request,'auths/activatefail.html')

def login(request):
    
    if request.method== "POST":
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=email)
        if not user_obj.exists():
            messages.error(request,"No User found")
            return HttpResponseRedirect(request.path_info)

        user_obj=authenticate(username=email, password=password)

        if user_obj:
            auth_login(request, user_obj)
            return redirect('/')
        else:
            messages.warning(request,"invalid credational")
            return HttpResponseRedirect(request.path_info)
    
    return render(request,'auths/login.html')
def handleout(request):
    logout(request)
    messages.success(request,"logout successfully")
    
    return redirect('/ecomauth/login')