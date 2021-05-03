from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 登陆相关
    # include需要两个参数，arg和namespace
    # 当namespace不为空时，arg参数必须是一个2元组
    # 除了urlpatterns不能为空之外，app_name也必须填写
    path('login/', include(('login.urls', 'login'), namespace='login')),

    # 登陆成功后主界面
    path('index', include('mainpage.urls'))
]
