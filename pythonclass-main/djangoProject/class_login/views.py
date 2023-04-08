import datetime
import os
import re
import tempfile
import time

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
import json
from .utils import fetch_nodes,ResetPassword
# 导入用于装饰器修复技术的包
from functools import wraps

logger = logging.getLogger('collect')


# 装饰器函数，用来判断是否登录
def check_login(func):
    @wraps(func)  # 装饰器修复技术
    def inner(request, *args, **kwargs):
        ret = request.session.get("is_login")
        # 获取当前的url,类型是string
        next_url = request.path_info
        s_list = next_url.split('/')
        # 1. 获取cookie中的随机字符串
        # 2. 根据随机字符串去数据库取 session_data --> 解密 --> 反序列化成字典
        # 3. 在字典里面 根据 is_login 取具体的数据
        # 如果是教师登录，并且是教师端的url，则直接进入相应界面
        if ret == "1" and ('teacher' in s_list):
            return func(request, *args, **kwargs)
        # 如果是教师登录，并且是教师端的url，则直接进入相应界面
        elif ret == "2" and ('student' in s_list):
            return func(request, *args, **kwargs)
        # 没有登录过
        else:
            # ** 即使登录成功也只能跳转到home页面，现在通过在URL中加上next指定跳转的页面
            return redirect("/login?next={}".format(next_url))
    return inner
# 登录函数
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.GET.get("next")
        # 这里设置为用户名和密码都是1，方便向数据库中添加信息。和下面的交替注释使用
        # if username == '1' and password == '1':
        # 如果登录的用户名和密码都是对应于教师端
        if username==fetch_nodes('Teacher')[0]['node_properties']['username'] and password==fetch_nodes('Teacher')[0]['node_properties']['password']:
            # 设置session 1代表是教师登录
            # ID是学生的学号或者是教师的登陆账户
            request.session["ID"] = username
            # name是姓名
            request.session["name"] = "蒋万春"
            request.session["is_login"] = "1"
            # session在关闭浏览器后失效
            request.session.set_expiry(0)
            # 如果有目标url
            if next_url:
                # 将url进行分词处理
                s_list = next_url.split('/')
                # 如果目标url中有teacher，则直接跳到目标url
                if 'teacher' in s_list:
                    rep = redirect(next_url)
                    return rep
                # 如果请求的是学生端的url，则直接跳到teacher的首页
                else:
                    return redirect('/teacher/')
                    # return render(request, 'teacher/index.html')
            # 如果没有目标url，则直接跳到teacher的首页
            else:
                return redirect('/teacher/')
                # return render(request, 'teacher/index.html')
        else:
            student_list = fetch_nodes('Student')
            # 遍历学生节点
            for l in student_list:
                if username==l['node_properties']['username'] and password==l['node_properties']['password']:
                    # 创建文件，记录学生的登录次数
                    # 记录学生的登录信息
                    t = time.strftime('%H:%M:%S', time.localtime())
                    today = datetime.date.today()
                    formatted_today = today.strftime('date_%y_%m_%d')
                    filename = './login_times/' + formatted_today + '.csv'
                    if not os.path.exists(filename):
                        with open(filename, 'w') as file_object:
                            file_object.write("登陆时间,登录学号,登陆姓名\n")
                    # 在session中记录学生的id和姓名
                    request.session["ID"] = username
                    request.session["name"] = l['node_properties']['name']
                    with open(filename, 'a') as object:
                        object.write(t + ',' + username + ',' + request.session["name"]+'\n')
                    # 设置session，2代表是学生
                    request.session["is_login"] = "2"
                    request.session.set_expiry(0)
                    # 通过URL中的next参数指定跳转的页面，如果为空，默认跳转到home页面
                    if next_url:
                        # 将url进行分词处理
                        s_list = next_url.split('/')
                        # 如果目标url中有student，则直接跳到目标url
                        if 'student' in s_list:
                            rep = redirect(next_url)
                            return rep
                            # 如果请求的是教师端的url，则直接跳到student的首页
                        else:
                            return redirect('/student/')
                            # return render(request, 'student/index.html')
                    # 如果没有目标url，则直接跳到teacher的首页
                    else:
                        return redirect('/student/')
                        # return render(request, 'student/index.html')
            # 如果一个学生和教师都对不上，就说明出错了。
            info = json.dumps('warning')
            context = {'warning':info}
            return render(request, 'class_login/index.html',context)
    return render(request, 'class_login/index.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        # 得到所有的学生节点，方便进行遍历
        student_list = fetch_nodes('Student')
        for l in student_list:
            if username == l['node_properties']['username'] and old_password == l['node_properties']['password']:
                if new_password1==new_password2:
                    ResetPassword(username,new_password1)
                    info = json.dumps('ok')
                    context = {'warning': info}
                    return render(request, 'class_login/index.html', context)
                else:
                    info = json.dumps('notsame')
                    context = {'warning': info}
                    return render(request, 'class_login/register.html', context)
        info = json.dumps('worng')
        context = {'warning': info}
        return render(request, 'class_login/register.html',context)
    return render(request, 'class_login/register.html')