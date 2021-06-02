from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticate_user(view_func):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        else:
            return view_func(request,*args,*kwargs)
    return inner

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def inner(request,*args,**kwargs):
            role = None
            if request.user.is_admin:
                role = 'Admin'

            else:
                role = 'Customer'
                
            if role in allowed_roles:
                return view_func(request,*args,*kwargs)
            else:
                messages.info(request,'you are not allowed')
                return redirect('login')
        return inner
    return decorator
