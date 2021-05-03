from django.urls import path
from login import views

urlpatterns = [
    path('', views.login, name='login_page'),  # href = "{% url 'login:login_page' 1 2 %}"  from django.core.urlresolvers import reverse url = reverse('login:login_page', args=(1,2, ...))
    path('regist', views.regist),
    path('regist_check', views.regist_check),
    path('login_check', views.login_check),
    path('verify_code', views.verify_code),
]
