from .forms import RegisterForm, LoginForm
from .models import User
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import login, authenticate
from utils import restful


class register_view(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            user = User.objects.create_user(username=username, telephone=telephone, password=password, email=email)
            login(request, user)
            return restful.ok()
        else:
            errors = form.get_errors()
            return restful.params_error(message=errors)


class login_view(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            # user = authenticate(request, telephone=telephone, password=password)
            user = User.objects.filter(username=username, telephone=telephone).first()
            checked = user.check_password(password)
            if checked:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    return restful.ok()
                else:
                    return restful.unauth(message='你已经被拉黑了!')
            else:
                return restful.unauth(message='账号或密码错误')
        else:
            errors = form.get_errors()
            return restful.params_error(data=errors)


def logout(request):
    request.session.flush()
    return redirect(reverse('blog:index'))
