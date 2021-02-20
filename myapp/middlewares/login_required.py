from django.shortcuts import render,redirect
from django.urls import path

def login_required(get_response):
    def middleware(request,product_id=None):
        user=request.session.get('user')
        if user:
            response=None
            if product_id:
                response=get_response(request,product_id)
            else:
                response=get_response(request)
            return response
        else:
            url=request.path
            return redirect(f'/login?return_url={url}')
    return middleware