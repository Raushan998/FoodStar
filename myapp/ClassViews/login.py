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


class Login(View):
    return_url=None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'login.html')
    def post(self,request):
        try:
            email=request.POST.get('email')
            password=request.POST.get('password')
            customer=User.objects.get(email=email)
            flag=check_password(password,customer.password)
            if flag:
                user={}
                user['email']=email;
                print(user)
                request.session['user']=user
                if Login.return_url:
                    return redirect(Login.return_url)
                return redirect('index')
            else:
                return render(request,'login.html',{"message":"Enter correct password!"})
        
        except:
            return render(request,'login.html',{"message":"Email doesn't exist"})


def logout(request):
    request.session.clear()
    return redirect('index')
