from django.db import models
from django.conf import settings


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20, null=True)


class Category(models.Model):
    name = models.CharField(max_length=20, null=True)


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    desc = models.CharField(max_length=500, null=True)
    tag = models.ManyToManyField('Tag')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey('Article',on_delete=models.CASCADE,null=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-pub_time']