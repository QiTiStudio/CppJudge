from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from login import models
import re
from PIL import Image, ImageDraw, ImageFont
from six import BytesIO


EXCLUDE_IPS = []


# ip封禁装饰器  中间件的实现方式更加优雅
def blocked_ip(view_func):
    def wrapper(request, *args, **kwargs):
        # 获取对方ip
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in EXCLUDE_IPS:
            return HttpResponse("<h1>You are banned for some reasons.</h1>")
        else:
            # 这里必须写成return
            return view_func(request, *args, **kwargs)
    return wrapper


# 加载登录界面
def login(request):
    return render(request, 'login/ajax_login.html')


# 在数据库中验证登陆
def verify_in_db(username, password):
    queryset = models.UserInfo.objects.filter(username=username)
    if queryset.count() == 1:
        if queryset[0].password == password:
            return True
    return False


# 登陆验证
def login_check(request):
    # 接收post请求
    query_dic = request.POST
    username = query_dic.get('name')
    password = query_dic.get('psw')
    vc = query_dic.get('vc')
    # 判断是否符合登陆要求
    if_success = False
    # 首先判断验证码
    if(vc == request.session.get('verifycode', None)):
        # 再判断用户名和密码
        if_success = verify_in_db(username, password)
    # 返回json
    response = {'res': if_success}
    return JsonResponse(response)


# 注册信息验证
def username_verify(name, info):
    result = True
    if len(name) < 6:
        info.append('用户名不能小于6个字符')
        result = False
    if re.match('^[0-9a-zA-Z_]{1,}$', name) is None:
        info.append('用户名只能由字母数字下划线组成')
        result = False
    return result


def password_verify(psw, repsw, info):
    result = True
    if psw is None or len(psw) < 6:
        info.append('密码不能小于6个字符')
        result = False
    if repsw != psw:
        info.append('重复密码和原密码不符')
        result = False
    return result


# 在数据库中注册
def regist_in_db(info_dic):
    models.UserInfo.objects.create(info_dic)


# 注册信息合法性检查器
def regist_check(request):
    info_dic = request.POST
    name = info_dic.get('username')
    psw = info_dic.get('password')
    repsw = info_dic.get('repassword')
    info = []
    name_ok = username_verify(name, info)
    psw_ok = password_verify(psw, repsw, info)
    # 判断是否成功注册
    if name_ok and psw_ok:
        regist_in_db(info_dic)
        return JsonResponse({'res': True})
    else:
        # 整理错误信息
        err_info = info[0]
        for i in range(1, len(info)):
            err_info += (" 且 " + info[i])
        return JsonResponse({'res': False, 'info': err_info})


# 加载注册页面
def regist(request):
    return render(request, 'login/regist.html')


# 验证码生成
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景、长宽高
    bgcolor = (255, 255, 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 绘制底噪点
    for i in range(0, 30):
        now_xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        for j in range(10):
            now_xy = (now_xy[0]+random.randrange(-1, 2), now_xy[1]+random.randrange(-1, 2))
            draw.point(now_xy, fill=fill)
    # 定义验证码的备选值
    strl = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += strl[random.randrange(0, len(strl))]
    # 构造字体对象， ubuntu的字体路径为"/usr/share/fonts/truetype/freefont"
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 绘制4个字
    for i in range(4):
        font = ImageFont.truetype('FreeMono.ttf', random.randrange(23, 30))
        fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.text((5+25*i, 2), rand_str[i], font=font, fill=fontcolor)
    # 绘制顶噪点1 斜线
    for i in range(0, 10):
        now_xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        for j in range(20):
            now_xy = (now_xy[0]+random.randrange(-1, 1), now_xy[1]+random.randrange(-1, 1))
            draw.point(now_xy, fill=fill)
    # 绘制顶噪点2 竖线
    for i in range(0, 10):
        start_xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        # 长度宽度
        ll = random.randrange(5, 20)
        ww = random.randrange(1, 2)
        for j in range(0, ll):
            for k in range(0, ww):
                xy = (start_xy[0] + k, start_xy[1] + j)
                draw.point(xy, fill=fill)
    # 绘制顶噪点3 白点
    for i in range(0, 500):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (255, 255, 255)
        draw.point(xy, fill=fill)
    # 释放画笔
    del draw
    # 存入session， 用于作进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型是png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为png
    return HttpResponse(buf.getvalue(), 'image/png')
