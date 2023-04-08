from django.urls import path, re_path
from student import views

urlpatterns = [
    # 有页面内容的返回
    path('hello', views.hello_world),
    re_path(r'^$', views.index),
    # re_path(r'^add_knowledge$',views.add_knowledge),
    re_path(r'^add_test$',views.add_test),
    re_path(r'^finish_test$', views.finish_test),
    # 返回确定的测试界面
    re_path(r'^certain_test$', views.certain_test),
    # 自行进行模拟测试
    re_path(r'^mock_test$', views.mock_test),
    re_path(r'^create_mock$', views.create_mock),
    # re_path(r'^create_examination$', views.create_examination),
    # re_path(r'^view_test$', views.view_test),

    # 没有页面内容返回的view
    # re_path(r'^addKnowledge2Neo$', views.addKnowledge2Neo),
    re_path(r'^addTest2Neo$', views.addTest2Neo),
    # re_path(r'^fetch_paper$', views.fetch_test_in_neo),
    # re_path(r'^delete_node$', views.delete_node),
    # re_path(r'^renew$', views.renew_node),
    re_path(r'^code$', views.runcode),
    re_path(r'^blank_code$', views.runblank_code),
    re_path(r'^findtest$', views.FindTest),
    re_path(r'^homeworksubmit$', views.HWSubmit),

]