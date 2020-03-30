from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, username, password, telephone, **kwargs):
        if not username:
            raise ValueError('请输入手机号码')
        if not password:
            raise ValueError('请输入密码')
        if not telephone:
            raise ValueError('请输入手机号码')
        user = self.model(username=username, telephone=telephone, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, telephone, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username=username, telephone=telephone, password=password, **kwargs)

    def create_superuser(self, username, password, telephone, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(username=username, telephone=telephone, password=password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=20)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(null=True, unique=True)
    date_join = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    # 用作验证,django默认为username
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

