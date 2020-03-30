from django.shortcuts import render
from apps.blog.models import Category, Article, Tag
from utils import restful
from django.views.generic import View
from .forms import ArticleForm
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from utils.decorators import staff_required, cms_required
from django.contrib.admin.views.decorators import staff_member_required


@method_decorator(permission_required(perm='article.add_article', login_url='/'), 'dispatch')
class write_article(View):
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            categoryId = form.cleaned_data.get('category')
            category = Category.objects.get(pk=categoryId)
            Article.objects.create(title=title, content=content, category=category, author=request.user,
                                   desc=desc)
            return restful.ok()
        else:
            return restful.params_error(message='不能为空')


@method_decorator(permission_required(perm='article.change_article', login_url='/'), 'dispatch')
class edit_article(View):
    def get(self, request):
        article_id = request.GET.get('article_id')
        article = Article.objects.get(pk=article_id)
        categories = Category.objects.all()
        context = {
            'article': article,
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_id = request.POST.get('pk')
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            categoryId = form.cleaned_data.get('category')
            category = Category.objects.get(pk=categoryId)
            Article.objects.filter(pk=article_id).update(title=title, desc=desc, content=content, category=category)
            return restful.ok()
        else:
            return restful.params_error(form.get_errors())


@method_decorator(permission_required(perm='article.change_article', login_url='/'), 'dispatch')
class article_list(View):
    # request 获取的所有数据都是字符串类型
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # 默认值只有没有传递参数的时候使用,如果传递,即使是空字符串也不会使用默认值
        category_id = int(request.GET.get('category', 0))
        articles = Article.objects.select_related('category', 'author')
        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2020, month=1, day=1)
            if end:
                print(end)
                end_date = datetime.strptime(end, '%Y/%m/%d')
                print(end_date)
            else:
                end_date = datetime.today()
            articles = articles.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            articles = articles.filter(title__icontains=title)
        if category_id:
            articles = articles.filter(category=category_id)

        # 传入所有对象,以及对对象分片
        paginator = Paginator(object_list=articles, per_page=2)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)
        context = {
            'categories': Category.objects.all(),
            'articles': page_obj.object_list,
            'category_id': category_id,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'page_obj': page_obj,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or '0',
            })
        }
        # 与列表extend类似
        context.update(context_data)
        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@permission_required(perm='article.delete_article', login_url='/')
def del_article(request):
    article_id = request.POST.get('pk')
    Article.objects.get(id=article_id).delete()
    return restful.ok()
