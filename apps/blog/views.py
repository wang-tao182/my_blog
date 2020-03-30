from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category, Article, Comment
from utils import restful
from .serializer import CommentSerializers
from utils.decorators import blog_login_required


# Create your views here.
@ensure_csrf_cookie
def index(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    context = {
        'categories': categories,
        'articles': articles
    }
    return render(request, 'index.html', context=context)


def article_detail(request, article_id):
    print(article_id)
    article = Article.objects.select_related('author', 'category').prefetch_related('comment_set').get(pk=article_id)
    categories = Category.objects.all()
    context = {
        'article': article,
        'categories': categories,
    }
    return render(request, 'article_detail.html', context=context)


@blog_login_required
def comment(request):
    try:
        content = request.POST.get('content')
        pk = request.POST.get('pk')
        article = Article.objects.get(pk=pk)
        comment = Comment.objects.create(content=content, author=request.user, article=article)
        serializer = CommentSerializers(comment)
        print(serializer)
        print("+++++++")
        data = serializer.data
        # data 为字典
        return restful.result(data=data)

    except:
        return restful.params_error(message='评论格式错误')

# data = {'pub_time': '2020-03-30T23:46:39.605343+08:00', 'content': '1', 'id': 68, 'author': OrderedDict(
#     [('uuid', 'meDCdoFbj52oQX7rvaeic8'), ('telephone', '13938499083'), ('username', '王涛'), ('is_staff', True),
#      ('email', '1769710004@qq.com'), ('is_active', True)])}

