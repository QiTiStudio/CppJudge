from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class IpBlockedMiddleware(MiddlewareMixin):
    EXCLUDE_IPS = []

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """执行视图函数前会调用该函数"""
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in IpBlockedMiddleware.EXCLUDE_IPS:
            return HttpResponse("<h1>You are banned for some reasons.</h1>")


# 设置完记得去settings里注册 MIDDLEWARE_CLASSES
class ExampleMiddleware(MiddlewareMixin):
    '''中间件类'''
    def __init__(self):
        '''服务器重启后，接收第一个请求时调用'''

    def process_request(self, request):
        '''产生request对象后，url匹配前调用'''
        # 这里return可以直接终止流程，跳转到process_response
        return HttpResponse("<h1>shut</h1>")

    def process_view(self, request, view_func, *args, **kwargs):
        '''url匹配之后，视图函数调用之前调用'''
        # 这里return可以直接终止流程，不再执行view_func跳转到process_response
        return HttpResponse("<h1>shut</h1>")

    def process_response(self, request, response):
        '''视图函数调用之后， 内容返回浏览器之前'''
        return response

    def process_exception(self, request, exception):
        '''视图函数发生异常时调用
        注意：如果多个中间件包含process_exception调用顺序和注册顺序是相反的'''
        print(exception)
