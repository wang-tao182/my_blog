from django import forms
from .models import User
from apps.forms import FormMixin


class RegisterForm(forms.Form, FormMixin):
    username = forms.CharField(max_length=20)
    telephone = forms.CharField(max_length=11, error_messages={'max_length': '电话号码必须为11位'})
    email = forms.EmailField()
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': '密码长度不超过11位', 'min_length': '密码长度最短11位'})
    repeat_password = forms.CharField(max_length=20, min_length=6)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if repeat_password != password:
            raise forms.ValidationError('两次密码输入不一致')


class LoginForm(forms.Form, FormMixin):
    remember = forms.IntegerField(required=False)
    username = forms.CharField()
    telephone = forms.CharField(max_length=11, error_messages={'max_length': '电话号码必须为11位'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': '密码长度不超过11位', 'min_length': '密码长度最短11位'})
