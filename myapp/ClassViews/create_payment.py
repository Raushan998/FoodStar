from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from myapp.ClassViews import product_listing
from myapp.models.orders import Order
from myapp.models.Users import User
from django.views import View
from foodApp.settings import API_KEY,AUTH_TOKEN
import random
from instamojo_wrapper import Instamojo
import math
api=Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,
              endpoint='https://test.instamojo.com/api/1.1/')


def CreatePayment(request):
    user=request.session.get('user')
    total_sum=0
    cart=request.session.get('cart')
    if cart:
        for item in cart.keys():
            product=Product.objects.get(id=item)
            total_sum += math.floor(product.price-(product.price *
                                                product.discount_price)/100)*int(cart[item])
        amount=math.floor(total_sum)
        response=api.payment_request_create(
            amount=amount,
            purpose="For Food",
            send_email=True,
            email=user.get('email'),
            redirect_url="https://foodstar345.herokuapp.com/complete-payment"
        )
        print(response)
        payment_request_id=response['payment_request']['id']
        user['payment_request_id']=payment_request_id
        print(request.session.get('user'))
        
        request.session['user']=user
        url=response['payment_request']['longurl']
        return redirect(url)
    else:
        return redirect('listing')

def verfiyPayment(request):
    user=request.session.get('user')
    payment_id = request.GET.get('payment_id')
    payment_request_id = request.GET.get('payment_request_id')
    response = api.payment_request_payment_status(
        payment_request_id, payment_id)
    
    print(response)
    status = response['payment_request']['payment']['status']
    if status=='Credit' and user.get('payment_request_id')==payment_request_id:
        cart=request.session.get('cart')
        for item in cart.keys():
            if cart.get(item):
                email = user.get('email')
                address = user.get('address')
                phone = user.get('phone')
                customer = User.objects.get(email=email)
                product=Product.objects.get(id=item)
                price=math.floor(product.price-(product.price*product.discount_price)/100)*int(cart.get(item));
                quantity=cart[item]
                order=Order(customer=customer,product=product,
                            address=address,phone=phone,
                                price=price,quantity=quantity,
                                    payment_id=payment_id,payment_request_id=payment_request_id,
                                        status=True)
                order.save()
        cart={}
        request.session['cart']=cart;
        return redirect('summary')
    else:
        message={
            "message": "Payment Unsuccessful please try again!"
        }
        request.session['message']=message;
        return redirect('checkout')


def Summary(request):
    user=request.session.get('user')
    email=user.get('email')
    customer=User.objects.get(email=email)
    summary=Order.objects.filter(customer=customer).order_by('-date')
    context={
        'summary':summary
    }
    return render(request,'order.html',context)
