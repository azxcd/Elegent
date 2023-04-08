from django.urls import path, re_path
from teacher import views

urlpatterns = [
    # 有页面内容的返回
    path('hello', views.hello_world),
    re_path(r'^$', views.index),
    re_path(r'^add_knowledge$',views.add_knowledge),
    re_path(r'^add_test$',views.add_test),
    re_path(r'^create_paper$', views.create_paper),
    re_path(r'^create_examination$', views.create_examination),
    re_path(r'^view_test$',views.view_test),
    # 小测完成情况
    re_path(r'^test_info$',views.test_info),
    # 查看班级学习情况
    re_path(r'^class_info$',views.CheckClassInfo),
    # 查看某个学生的学习情况
    re_path(r'^stu_info$',views.CheckStuInfo),

    # 没有页面内容返回的view
    re_path(r'^addKnowledge2Neo$', views.addKnowledge2Neo),
    re_path(r'^addTest2Neo$', views.addTest2Neo),
    re_path(r'^fetch_paper$',views.fetch_test_in_neo),
    re_path(r'^delete_node$',views.delete_node),
    # 修改知识节点
    re_path(r'^renew$',views.renew_node),
    # 修改题目节点
    re_path(r'^renewtest$',views.renew_testnode),
    # 创建指定内容的作业
    re_path(r'^create_homework$',views.CreateHomework),
    # re_path(r'^code$',views.runcode),
    # re_path(r'^choice$',views.check_choice),
    # re_path(r'^blank$',views.check_blank),
]