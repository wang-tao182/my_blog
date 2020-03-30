from apps.blogauth.models import User
from django.shortcuts import redirect, reverse
from . import restful
from functools import wraps
from django.shortcuts import Http404


def cms_required(func):
    def wrapper(request, *args, **kwargs):
        auth_user_id = request.session.get('_auth_user_id')
        if auth_user_id:
            user = User.objects.get(pk=auth_user_id)
            if user:
                if user.is_staff:
                    return func(request, *args, **kwargs)
                else:
                    return redirect(reverse('blog:index'))
            else:
                return redirect(reverse('blog:index'))
        else:
            return redirect(reverse('blog:index'))

    return wrapper


def blog_login_required(func):
    def wrapper(request, *args, **kwargs):
        auth_user_id = request.session.get('_auth_user_id')
        if auth_user_id:
            user = User.objects.get(pk=auth_user_id)
            if user:
                return func(request, *args, **kwargs)
            else:
                if request.is_ajax():
                    return restful.unauth(message='请先登录')
                else:
                    return redirect(reverse('blogauth:login'))
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录')
            else:
                return redirect(reverse('blogauth:login'))
    return wrapper


def superuser_required(viewfunc):
    @wraps(viewfunc)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper


def staff_required(viewfunc):
    @wraps(viewfunc)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper

