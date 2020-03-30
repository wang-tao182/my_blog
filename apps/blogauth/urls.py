from django.urls import path
from . import views

app_name = 'blogauth'

urlpatterns = [
    path('signup/', views.register_view.as_view(), name='register'),
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]
