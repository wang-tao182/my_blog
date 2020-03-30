from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
from apps.blog.models import Article, Comment, Category

# 这里主要是权限与组的绑定,多对多
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 编辑分组(管理文章,管理课程,轮播图)
        # 通过模型获得content_type用get_for_model(self, model, for_concrete_model=True)
        edit_content_types = [
            # contenttype实例
            ContentType.objects.get_for_model(Article),
            ContentType.objects.get_for_model(Category),
        ]
        # Permission 权限类
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        editGroup = Group.objects.create(name='编辑')
        # permissions与Permission多对多映射
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('编辑分组创建完成'))
        # 财务组(课程订单,付费咨询订单)
        finance_content_types = [
            ContentType.objects.get_for_model(Comment)
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        financeGroup = Group.objects.create(name='评论')
        # 外键多对多
        financeGroup.permissions.set(finance_permissions)
        print(financeGroup.permissions)
        financeGroup.save()
        self.stdout.write(self.style.SUCCESS('评论分组创建完成'))

        # 管理组(编辑组+财务组)
        admin_permissions = edit_permissions.union(finance_permissions)
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS('管理员分组创建完成'))

        # 超级管理员
