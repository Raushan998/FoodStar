from myapp.models.Users import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from myapp.utils.email_sender import sendEmail
import math
import random
import re


class ForgetPassword(View):
    def get(self,request):
        return render(request,'forget_email.html',{"step_1":True})
    def post(self,request):
        try:
            email=request.POST.get('email')
            user=User.objects.get(email=email)
            otp=math.floor(random.random()*100000);
            name=user.first_name
            html=f'''
                    Hi {user.first_name} your otp for reset password is {otp}.
                    '''
            request.session['verification-code']=otp;
            request.session['email']=email;
            response = sendEmail(name=name, email=email,
                                    subject="Otp for password resetting", htmlcontent=html)
            message = "Otp has been sent at your email."
            return render(request,'forget_email.html',{'step_2':True,"message":message})
        except:
            message="Email doesn't exist"
            return render(request,'forget_email.html',{'step_1':True,"message":message})
        
        
def OTPVerification(request):
    if request.method=="POST":
        current_otp=request.POST.get('otp')
        otp=request.session.get('verification-code')
        if str(otp)== str(current_otp):
            return render(request,'forget_email.html',{'step_3':True})
        else:
            message=" Otp doesn't match."
            return render(request,'forget_email.html',{'step_2':True,"message":message})


def PasswordVerification(request):
    if request.method=='POST':
        password=request.POST.get('password-1')
        confirm_password=request.POST.get('password-2')
        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        result = re.findall(pattern, password)
        if password != confirm_password:
            message=" password and confirm password doesn't match."
            return render(request,'forget_email.html',{'step_3':True,'message':message})
        elif not result:
            message=" password should be strong. use @,_,#"
            return render(request,'forget_email.html',{'step_3':True,'message':message})
        else:
            email=request.session.get('email')
            user=User.objects.get(email=email)
            user.password=make_password(password)
            user.save()
            message="Your password has been reset."
            return render(request,'login.html',{"message":message,"step_2":True})

