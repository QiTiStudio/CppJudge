from django.contrib import admin
from login import models


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'isDelete']


admin.site.register(models.UserInfo, UserInfoAdmin)
