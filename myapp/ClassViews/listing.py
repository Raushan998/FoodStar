from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from myapp.ClassViews.choices import get_location

class Listing(View):
    def get(self,request):
        current_location=request.session.get('location')
        if current_location:
            location = Location.objects.get(location=current_location.get('location'))
            product = Product.objects.filter(location=location)
            if 'item' in request.GET:
                item = request.GET['item']
                product=product.filter(name__icontains=item)
            
            paginator = Paginator(product,6)
            page = request.GET.get('page')
            paged_listing = paginator.get_page(page)
            context = {
                'products': paged_listing
            }
            return render(request, 'listing.html', context)
        else:
            return redirect('index')
    
    def post(self,request):
        current_location = request.POST.get('location')
        print(current_location)
        if not current_location:
            message="please enter the location"
            return render(request, 'index.html', {"message":message,'location':get_location})
        try:
            location = Location.objects.get(location=current_location)
            product = Product.objects.filter(location=location)
            temp = request.session.get('location')
            if temp:
                if temp['location'] != location.location:
                    temp['location'] = location.location
                    request.session['location'] = temp
                    cart = request.session.get('cart')
                    if cart:
                        del request.session['cart']
                        cart = {}
                        request.session['cart'] = cart

            else:
                temp = {}
                temp['location'] = location.location
                request.session['location'] = temp
            paginator=Paginator(product,6)
            page=request.GET.get('page')
            paged_listing=paginator.get_page(page)
            context = {
                'products': paged_listing
            }
            return render(request, 'listing.html', context)
        except:
            return HttpResponse("<h1>Sorry! we are not available here</h1>")
