from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from myapp.ClassViews.choices import get_location


def index(request):
    cart = request.session.get('cart')
    if not cart:
        cart={}
        request.session['cart'] = cart
    return render(request, 'index.html',{'location':get_location})
