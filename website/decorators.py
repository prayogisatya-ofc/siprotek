from django.shortcuts import redirect
from . import models as db
from django.http import HttpResponse
from django.contrib.auth import logout

def allowed_users(roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = db.User.objects.filter(uuid=request.user)
            if user[0].role in roles:
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return redirect("/")
        return wrapper_func
    return decorator