from django.urls import path, re_path
from class_login import views

urlpatterns = [
    # 有页面内容的返回
    re_path(r'^$', views.login),
    re_path(r'^login$', views.login),
    re_path(r'^register$', views.register),

    # 没有页面内容返回的view
    # re_path(r'^addKnowledge2Neo$', views.addKnowledge2Neo),
    ]