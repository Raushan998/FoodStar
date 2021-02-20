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

class SendOTP(View):
    def get(self,request):
        return render(request,'signup.html',{'step_1':True})
    def post(self,request):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone')
            password = request.POST.get('password-1')
            confirm_password=request.POST.get('password-2')
            customer=User(first_name=first_name,last_name=last_name,
                            email=email,password=password,phone_number=phone_number);
            value={
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'phone_number':phone_number
            }
            error_message=None
            error_message=self.ValidateForm(customer)
            if error_message:
                return render(request,'signup.html',{'message':error_message,'value':value,'step_1':True})
            else:
                if password!=confirm_password:
                    return render(request,'signup.html',{'message':"Password doesn't match",'value':value,'step_1':True})
                temp={
                    'first_name':first_name,
                    'last_name':last_name,
                    'email':email,
                    'phone_number':phone_number,
                    'password':password
                    }
                request.session['profile']=temp
                otp = math.floor(random.random()*100000)
                html=f'''
                        Hi {first_name}
                        <h4>Your verification code is {otp}</h4>
                    '''
                name=first_name
                print(email)
                response=sendEmail(name=name,email=email,
                                    subject="Regarding Otp for account_opening",htmlcontent=html)
                request.session['otp']=otp
                message="OTP has been sent at your email"
                return render(request,'signup.html',{'step_2':True,"message":message})
        except:
            message = " your account can't be created!"
            return render(request, 'signup.html', {'message': message, 'step_1': True})
            

    def ValidateForm(self,customer):
        error_message=None
        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        result = re.findall(pattern, customer.password)
        if not customer.first_name:
            error_message="Please enter first name"
            return error_message
        elif not customer.email:
            error_message="please enter email"
            return error_message
        elif not customer.phone_number:
            error_message="Please enter phone number"
            return error_message
        elif not customer.password:
            error_message="please enter password"
            return error_message
        elif customer.isExists():
            error_message='Email already registered'
        elif not result:
            error_message = "password should be strong. use @,_,#"
        elif not re.search(regex,customer.email):
            error_message=" please enter valid email"
        return error_message

class CheckOTP(View):
    def post(self,request):
        try:
            otp=request.session.get('otp')
            current_otp=request.POST.get('otp')
            print(otp)
            print(current_otp)
            if int(otp)==int(current_otp):
            
                profile=request.session.get('profile')
                first_name=profile['first_name']
                last_name=profile['last_name']
                email=profile['email']
                password=profile['password']
                password=make_password(password)
                phone_number=profile['phone_number']
                user=User(first_name=first_name,last_name=last_name,
                            email=email,password=password,
                                    phone_number=phone_number)
                user.save()
                del request.session['profile']
                del request.session['otp']
                print('acount created successful!')
                message="Your account has been created"
                return render(request,'login.html',{"message":message,"step_1":True})
            
            else:
                error_message="Please enter correct otp"
                return render(request,'signup.html',{'step_2':True,"message":error_message})
        except:
            message="You have already an account"
            return render(request, 'login.html', {"message": message, "step_1": True})


                


