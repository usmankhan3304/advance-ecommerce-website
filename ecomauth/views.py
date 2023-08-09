from django.shortcuts import render,HttpResponse,redirect
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
from .utils import TokenGenerator

#for emial 

from django.core.mail import send_mail
from django.conf import settings

# Create your views here

def signup(request):
    token=TokenGenerator()
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
        current_site=get_current_site(request)
        email_subject="please activate your account"
        message=render_to_string('ecomauth/activate.html',{
            'user':user_obj,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_decode(force_bytes(user_obj.pk)),
            'token':token.make_token(user_obj) 
        })
        email_from=message.settings.EMAIL_HOST_USER
        email_message=EmailMessage(email_subject,message,email_from)
        EmailThread(email_message).start()
        messages.info(request,"register successfully please login now " )
        return redirect('/ecomauth/login')
            
            
    return render(request,'auths/signup.html')
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