from django import forms
from apps.blog.models import Article
from apps.forms import FormMixin


class ArticleForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = Article
        exclude = ['category', 'pub_time', 'author', 'tag']
