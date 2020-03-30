from django.urls import path
from . import views
from . import write_views
app_name = 'cms'

urlpatterns = [
    path('', views.cms_index, name='cms_index'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/', views.article_category, name='category'),
    path('del_category/', views.del_category, name='del_category'),
    path('edit_category/', views.edit_category, name='edit_category'),
    path('write_article/', write_views.write_article.as_view(), name='write_article'),
    path('article_list/', write_views.article_list.as_view(), name='article_list'),
    path('del_article/', write_views.del_article, name='del_article'),
    path('edit_article/', write_views.edit_article.as_view(), name='edit_article'),
    path('add_staff/', views.add_staff.as_view(), name='add_staff'),
    path('staff/', views.staff, name='staff'),
]