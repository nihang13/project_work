import re

from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import PasswordChangeForm
#Send Mail
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string

from .models import Touch
from .models import Momo
# Create your views here.
date=datetime.now()

def index(request):
    ''''''
    buff=Momo.objects.filter(category="buff")
    veg=Momo.objects.filter(category="veg")
    chicken=Momo.objects.filter(category="chicken")
    
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
            

        Touch.objects.create(name=name, email=email, phone=phone, message=message)
            
        subject="Django Training"
        message=render_to_string('main/msg.html',{'name':name,'date':date})
        from_email="mai.studionp@gmail.com"
        recipient_list=[email]
            
        email_msg=EmailMessage(subject,message,from_email,recipient_list)
        email_msg.send(fail_silently=True)
        return redirect('index')
        #return HttpResponse("Message sent Successfully")
    return render(request,'main/index.html',{'date':date,'buff':buff,'chicken':chicken,'veg':veg})
'''
==========================================================
==========================================================
==========================================================
'''
@login_required(login_url='log_in')
def about(request):
    '''about page'''
    return render(request,'main/about.html')
def contact(request):
    '''contact page'''
    return render(request,'main/contact.html')
def menu(request):
    '''menu of restaurant'''
    return render(request,'main/menu.html')
def service(request):
    '''service provided'''
    return render(request,'main/services.html')
'''
===============================================
===============================================
            Authentication Part
===============================================
===============================================
'''
def register(request):
    '''register'''
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']        
        if password==password1:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username os already taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'email is already taken')
                    return redirect('request')
                elif not re.search(r'[A-Z]',password):
                    messages.error(request,'your password should contain atleast one uppercase')
                    return redirect('register')
                elif not re.search(r'\d',password):
                    messages.error(request,'your password should contain atleast one digit')
                    return redirect('register')
                elif not re.search(r'[!@#$%^&*()<>]',password):
                    messages.error(request,'your password must contain atleast one symbol')
                    return redirect('register')
                else:
                    User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    return redirect('log_in')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
        else:
            messages.error(request,'password doesnot match')
            return redirect('register')
    return render(request,'auth/register.html')

def log_in(request):
    '''login'''
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        remember_me=request.POST.get('remember_me')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register")
            return redirect('log_in')
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            if remember_me:
                request.session.set_expiry(1200000)
            else:
                request.session.set_expiry(0)
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Invalid Password")
            return redirect("log_in")
    return render(request,'auth/login.html')

def privacy(request):
    '''privacy'''
    return render(request,'main/privacy.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    '''change pw'''
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,'auth/change_password.html',{'form':form})
