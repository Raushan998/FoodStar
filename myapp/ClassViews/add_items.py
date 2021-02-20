from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from myapp.ClassViews import product_listing
# Create your views here.


def additems(request, item_id):
    
    if request.method == 'POST':
        item = request.POST.get('item')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            if remove:
                quantity = cart.get(remove)
                if quantity and quantity<=1:
                    cart.pop(remove)
                elif quantity and quantity>1:
                    cart[remove] = quantity-1
                else:
                    request.session['cart'] = cart
                    cateogary = request.session.get('cateogary')
                    return redirect(product_listing, cateogary['product_id'])

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
        # print(request.session.get('cart'))
        cateogary = request.session.get('cateogary')
        return redirect(product_listing, cateogary['product_id'])
