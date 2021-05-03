from django.db import models


# 用户表 管理器
class UserInfoManager(models.Manager):
    # 创建一个用户
    def create(self, info_dic):
        new_user = self.model()
        new_user.password = info_dic.get('password')
        new_user.username = info_dic.get('username')
        new_user.isDelete = False
        new_user.save()

    # 支持软删除的filter
    def filter(self, **kwargs):
        queryset = super().filter(**kwargs)
        queryset.filter(isDelete=False)
        return queryset


# 用户表
class UserInfo(models.Model):
    # 用户名 唯一
    username = models.CharField(max_length=20, null=False, primary_key=True)
    # 密码
    password = models.CharField(max_length=20, null=False)
    # 删除标记
    isDelete = models.BooleanField(default=False, null=False)

    objects = UserInfoManager()

    def __str__(self):
        return str(self.username)
