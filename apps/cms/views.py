from django.shortcuts import render, redirect, HttpResponse, reverse
from apps.blog.models import Category, Article
from apps.blogauth.models import User
from utils import restful
from django.contrib.auth.models import Group
from django.views.generic import View
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from utils.decorators import staff_required, cms_required, superuser_required
from django.contrib.admin.views.decorators import staff_member_required


@cms_required
def cms_index(request):
    return render(request, 'cms/index.html')


def article_category(request):
    categories = Category.objects.all()
    for category in categories:
        category.article_count = Article.objects.filter(category=category).count()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)


@permission_required(perm='category.add_category', login_url='/', )
def add_category(request):
    try:
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return restful.ok()
    except:
        return restful.params_error(message='未正确添加分类,请重新添加')


@permission_required(perm='category.delete_category', login_url='/', )
def del_category(request):
    category_id = request.POST.get('categoryId')
    Category.objects.get(id=category_id).delete()
    return restful.ok()


@permission_required(perm='category.change_category', login_url='/', )
def edit_category(request):
    try:
        name = request.POST.get('name')
        categoryId = request.POST.get('categoryId')
        # sql中也是执行update命令
        Category.objects.filter(pk=categoryId).update(name=name)
        return restful.ok()
    except:
        return restful.params_error(message='输入参数有误')


@method_decorator(superuser_required, name='dispatch')
class add_staff(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/add_staff.html', context=context)

    # 这里主要是组与用户的绑定 多对多
    def post(self, request):
        telephone = request.POST.get('telephone')

        user = User.objects.filter(telephone=telephone).first()
        if user:
            User.objects.filter(telephone=telephone).update(is_staff=1)
            staff = User.objects.get(telephone=telephone)
            groups_ids = request.POST.getlist('groups')
            groups = Group.objects.filter(pk__in=groups_ids)
            # groups多对多Group,set绑定
            staff.groups.set(groups)
            staff.save()
            return redirect(reverse('cms:staff'))
        else:
            return HttpResponse('该账号未注册')


@superuser_required
def staff(request):
    try:
        staffs = User.objects.filter(is_staff=True)
        context = {
            'staffs': staffs
        }
        return render(request, 'cms/staff.html', context=context)
    except:
        return restful.params_error(message='没有公司职员')

def staff2(request):
    pass
