from django.shortcuts import render
from .models import *
# Create your views here.
from django.contrib.auth.models import User
def home(request):
    data=User.objects.all()
    print(data)
    
    context={
        'data':data
    }    
    return render(request,'home/index.html',context)