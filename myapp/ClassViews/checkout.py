from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from myapp.ClassViews import product_listing
from myapp.models.orders import Order
from myapp.models.Users import User
from django.views import View


class Checkout(View):
    def get(self,request):
        try:
            print(request.session.get('cart'))
            current_location = request.session.get('location')
            location = Location.objects.get(location=current_location['location'])
            product=Product.objects.filter(location=location)
            cart=request.session.get('cart')
            step_1=False
            if cart:
                step_1=True
            message=request.session.get('message')
            user=request.session.get('user')
            email=user.get('email')
            get_user=User.objects.get(email=email)
            user_name=get_user.first_name;
            new_message=""
            if message:
                new_message=message.get('message')
                del request.session['message']
            print(user_name)
            if new_message!="":
                return render(request,'checkout.html',{'products':product,"step_1":step_1,'message':new_message,'user_name':user_name})
            else:
                return render(request, 'checkout.html', {'products': product, "step_1": step_1})
        except:
            return redirect('index')
    def post(self,request):
        try:
            cart=request.session.get('cart')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            current_location = request.session.get('location')
            location = Location.objects.get(location=current_location['location'])
            product = Product.objects.filter(location=location)
            user = request.session.get('user')
            email = user.get('email')
            get_user = User.objects.get(email=email)
            user_name = get_user.first_name
            if not address:
                message="please enter address"
                return render(request,'checkout.html',{'products':product,'step_1':True,"message":message,"user_name":user_name})
            elif not phone or (len(phone)<10 or len(phone)>13):
                message="please valid phone"
                return render(request, 'checkout.html', {'products': product, 'step_1': True, "message": message})
            else:
                user=request.session.get('user')
                user['address']=address
                user['phone']=phone
                request.session['user']=user
                # print(request.session.get('user'))
                return redirect('create-payment')
        except:
            return redirect('index')

def checkitems(request,item_id):
    if request.method == 'POST':
        item = request.POST.get('item')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            if remove:
                quantity = cart.get(remove)
                if quantity and quantity <= 1:
                    cart.pop(remove)
                elif quantity and quantity > 1:
                    cart[remove] = quantity-1
                else:
                    return redirect('checkout')

            else:
                quantity = cart.get(item)
                if quantity:
                    cart[item] = quantity+1
                elif item:
                    cart[item] = 1
        else:
            cart = {}
            if item:
                cart[item] = 1
        if cart:
            request.session['cart'] = cart
        return redirect('checkout')
