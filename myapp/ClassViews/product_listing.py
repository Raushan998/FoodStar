from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models.category import Location, Cateogary
from myapp.models.product import Product
from django.core.paginator import Paginator


def product_listing(request, product_id):
    try:
        current_location = request.session.get('location')
        location = Location.objects.get(location=current_location['location'])
        cateogary = Cateogary.objects.get(id=product_id)
        temp = request.session.get('cateogary')
        if temp:
            temp = {'product_id': product_id}
            request.session['cateogary'] = temp
        else:
            temp = {'product_id': product_id}
            request.session['cateogary'] = temp
        product = Product.objects.filter(
            cateogary=cateogary, location=location)
        paginator = Paginator(product,8)
        page = request.GET.get('page')
        paged_listing = paginator.get_page(page)
        context = {
            'products': paged_listing
        }
        
        # return HttpResponse("product Found")
        return render(request, 'product_listing.html', context)
    except:
        return HttpResponse('<h1>Sorry! we are not available here.<h1>')
    