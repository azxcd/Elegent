import os
import re

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
from .models import Knowledge,Theme,Point,Class,Test
import json
from .utils import fetch_nodes, add_k_node, add_t_node, create_tests, deleteN, renewN, fetch_all_nodes_title, \
    renewTestN, CheckStu, GetStuInfo, GetStuBaseInfo, GetStuHWInfo
from class_login.views import check_login
# 导入用于装饰器修复技术的包
from functools import wraps

# Create your views here.

logger = logging.getLogger('collect')

def hello_world(request):
    # 这里可以获得表单的数据
    nums = request.POST.getlist('nums','')
    node_names = request.POST.getlist('node_name','')
    return render(request,'teacher/hello_world.html',{})


# 添加题目结点
@check_login
def add_test(request):
    point_list = fetch_nodes('Point')
    p_l = []
    for p in point_list:
        p_l.append(p['node_properties']['title'])
    context = {'point_list': p_l}
    return render(request, 'teacher/add_test.html', context)

# 函数addTest2Neo用来处理表单提交后服务器响应的结果
def addTest2Neo(request):
    # 首先进行查重的功能，判断
    title_list = fetch_all_nodes_title()
    contents_list = fetch_nodes('Test')
    # 从前端返回的数据
    Type = request.POST['Type']
    difficulty = int(request.POST['Difficulty'])
    title = request.POST['title']
    importance = int(request.POST['Importance'])
    teached = int(request.POST['Teached'])
    homeworktimes = int(request.POST['HomeworkTimes'])
    wrongtimes = int(request.POST['WrongTimes'])
    examtimes = int(request.POST['ExamTimes'])
    father = request.POST.getlist('father','')
    question_text = request.POST['question_text']
    answer_text = request.POST['answer_text']
    for node in contents_list:
    #题目内容查重
        if node['node_properties']['attributes']['Content'].replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')==question_text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''):
            return render(request, 'teacher/wrong.html', {})
    for node in title_list:
    #题目节点查重
        if node.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')==title.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''):
            return render(request, 'teacher/error.html', {})
    context = {
        'Type': Type, 'difficulty': difficulty, 'title': title,
        'importance': importance, 'father': father,
        'teached': teached,'homeworktimes': homeworktimes,
        'wrongtimes': wrongtimes,'examtimes': examtimes,
        'question_text': question_text, 'answer_text': answer_text,
        }
    add_t_node(context)
    return render(request, 'teacher/hello_world.html', {})

# 添加知识节点
@check_login
def add_knowledge(request):#收到对应的url请求，跳到对应的界面
    class_list = fetch_nodes('Class')
    theme_list = fetch_nodes('Theme')
    knowledge_list = fetch_nodes('Knowledge')
    k_l = []
    t_l = []
    c_l = []
    for k in knowledge_list:
        k_l.append(k['node_properties']['title'])
    # logger.info(fetch_nodes('Knowledge')[0]['node_properties']['title'])
    for t in theme_list:
        t_l.append(t['node_properties']['title'])
    for c in class_list:
        c_l.append(c['node_properties']['title'])
    context = {'class_list':c_l,'theme_list':t_l,'knowledge_list':k_l}
    # logger.info(context['theme_list'])
    return render(request, 'teacher/add_knowledge.html', context)

# 函数add_knowledge2Neo用来处理表单提交后服务器响应的结果
def addKnowledge2Neo(request):
    # user = request.POST.get('user')
    type = request.POST['type']
    title = request.POST['title']
    # 进行插入节点的查重
    title_list = fetch_all_nodes_title()
    for node in title_list:
        if node.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')==title.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''):
            return render(request, 'teacher/wrong.html', {})
    difficulty = int(request.POST['Difficulty'])
    importance = int(request.POST['Importance'])
    mastery = int(request.POST['Mastery'])
    weights = int(request.POST['Weights'])
    teached = int(request.POST['Teached'])
    father = request.POST.getlist('father')
    for f in father:
        if f!='':
            father = f
            break
    context={'type':type,'difficulty':difficulty,'title':title,
             'importance':importance,'mastery':mastery,'father':father,
             'weights':weights,'teached':teached}
    # logger.info(context)
    add_k_node(context)
    return render(request, 'teacher/OK.html', {})

# 出卷功能的首页
@check_login
def create_paper(request):
    filename = 'all_test/'
    test_list = os.listdir(filename)
    # logger.info(test_list)
    all_test = {}
    for test_name in test_list:
        l = re.split('[._]', test_name)
        all_test[l[0]] = {}
        all_test[l[0]]['deadline'] = l[1]
        all_test[l[0]]['limittime'] = l[2]
    node_details_list = []
    node_details_list.extend(fetch_nodes('Class'))
    node_details_list.extend(fetch_nodes('Theme'))
    node_details_list.extend(fetch_nodes('Knowledge'))
    node_details_list.extend(fetch_nodes('Point'))
    node_details_list.extend(fetch_nodes('Test'))
    return render(request, 'teacher/create_paper.html', {'searchResult': json.dumps(node_details_list, ensure_ascii=False), 'all_test': all_test})

# 按教师要求在all_test文件夹中创建作业
def fetch_test_in_neo(request):
    # 得到对应的内容（test的节点名称和对应的出题数目）
    point_nums = request.POST.getlist('nums', '')
    points = request.POST.getlist('node_name', '')
    # 从前端获取作业的名称，时限和截止日期
    name = request.POST['title']
    timelimit = request.POST['timelimit']
    deadline = request.POST['deadline']
    logger.info(timelimit)
    test_dict = {}
    for i in range(len(points)):
        num = int(point_nums[i])
        if test_dict.__contains__(points[i]):
            test_dict[points[i]] = test_dict[points[i]]+num
        else:
            test_dict[points[i]] = num
    # logger = logging.getLogger('django')
    # logger.info(test_dict)
    # context是输入，里面的test_dict是字典，包含每个知识点的希望出题的数目。
    context = {'test_dict':test_dict}
    # 将内容保存为json
    b = json.dumps(context)
    # 在文件命名中加入作业名称_截止日期_完成时限信息
    f2 = open('all_test/'+name+'_'+str(deadline)+'_'+timelimit+'.json', 'w')
    f2.write(b)
    f2.close()
    # test_context也是一个字典，应该是{’choice‘:{'Content':[],'Answer':[]},’blank‘:{'Content':[],'Answer':[]},’code‘:{'Content':[],'Answer':[]}}
    # test_context = create_tests(context)
    # logger.info()
    # return render(request, 'teacher/check_test.html', test_context)
    # 重定向到教师端首页
    return redirect('/teacher/')

# 首页用来展示节点的具体数据
@check_login
def index(request):
    # 得到节点的数据
    node_details_list=[]
    node_details_list.extend(fetch_nodes('Class'))
    node_details_list.extend(fetch_nodes('Theme'))
    node_details_list.extend(fetch_nodes('Knowledge'))
    node_details_list.extend(fetch_nodes('Point'))
    node_details_list.extend(fetch_nodes('Test'))
    return render(request, 'teacher/index.html', {'searchResult':json.dumps(node_details_list, ensure_ascii=False)})

# 删除节点
def delete_node(request):
    # 得到要删除的节点的名字
    node_name = request.POST['name']
    logger.info(node_name)
    deleteN(node_name)
    return render(request, 'teacher/renew_success.html')


# 更新节点的信息
def renew_node(request):
    difficulty = request.POST['Difficulty']
    title = request.POST['title']
    importance = request.POST['Importance']
    weights = request.POST['Weights']
    teached = request.POST['Teached']
    renewN(title, difficulty, importance,weights,teached)
    return render(request, 'teacher/renew_success.html')

# 更新题目节点信息
def renew_testnode(request):
    difficulty = request.POST['Difficulty']
    title = request.POST['title']
    importance = request.POST['Importance']
    testtype = request.POST['Type']
    teached = request.POST['Teached']
    weights = request.POST['Weights']
    testanswer = request.POST['answer_text']
    testcontent = request.POST['question_text']
    renewTestN(title, testtype, difficulty, importance, teached, testanswer, testcontent)
    return render(request, 'teacher/renew_success.html')

# 创建试卷
@check_login
def create_examination(request):
    node_details_list = []
    node_details_list.extend(fetch_nodes('Class'))
    node_details_list.extend(fetch_nodes('Theme'))
    node_details_list.extend(fetch_nodes('Knowledge'))
    node_details_list.extend(fetch_nodes('Point'))
    node_details_list.extend(fetch_nodes('Test'))
    return render(request, 'teacher/create_examination.html', {'searchResult': json.dumps(node_details_list, ensure_ascii=False)})

# 教师预览试卷的功能
def view_test(request):
    # 得到对应的内容（test的节点名称和对应的出题数目）
    contents_list = request.POST.getlist('contents', '')
    answers_list = request.POST.getlist('answers', '')
    titles_list = request.POST.getlist('titles', [])
    logger.info(titles_list)
    test_context = {'content_list':contents_list,'answer_list':answers_list,'titles_list':json.dumps(titles_list)}
    return render(request, 'teacher/paper.html', test_context)

#教师端查看某个作业的完成情况
def test_info(request):
    # Context记录返回给前端的数据
    Context = {}
    # 首先从上一步中得到作业相关的信息
    # 读取前端传给后端的test_name和deadline
    test_name = request.POST['title']
    deadline = request.POST['deadline']
    limit_time = request.POST['limittime'][0:-3]
    # deadline = request.POST['deadline']
    # 读取前端传给后端的时间限制

    # 读取这个作业的文件内容:字典（{"test_dict": {"Point4": 2}}）
    file_name = 'all_test/' + test_name + '_' + deadline+'_'+limit_time+ '.json'
    with open(file_name, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    # 记录作业名称的数据
    Context['homework_name'] = test_name
    # 记录本次作业中包括的题目数量
    logger.info(json_data)
    if 'test_dict' in json_data.keys():
        Context['homework_dict'] = json_data['test_dict']
    else:Context['homework_dict'] = '固定题目'
    # 记录每个学生在本次小测中的得分
    stu_score, test_list = CheckStu(test_name)
    Context['stu_score'] = stu_score
    Context['test_list'] = test_list
    # Context['test_list'].append({'题目1':{'内容':'xxx','答案':'yyy','正确人数':10,'错误人数':2}})
    # Context['test_list'].append({'题目2':{'内容':'xxx2','答案':'yyy2','正确人数':9,'错误人数':0}})
    # # 记录本次作业的相关信息
    logger.info(Context)

    return render(request, 'teacher/test_info.html', Context)

# 查看班级的学习情况
def CheckClassInfo(request):
    # Context记录返回给前端的数据
    Context = {}
    # 得到所有的作业名称
    filename = 'all_test/'
    test_list = os.listdir(filename)
    # logger.info(test_list)
    all_test = []
    for test_name in test_list:
        l = re.split('[._]', test_name)
        all_test.append(l[0])

    Context['test_list'] = all_test
    # stu_info记录学生的相关信息,姓名,学号,每次作业得分等
    stu_info = GetStuInfo(all_test)
    Context['stu_info'] = stu_info
    # 还需要得到整个班级对Theme和Knowledge的掌握情况
    mastery = {}
    themes = fetch_nodes('Theme')
    for theme in themes:
        # logger.info(theme['node_properties']['title'])
        mastery[theme['node_properties']['title']] = {}
        # mastery[theme['node_properties']['title']]['val'] = theme['node_properties']['Mastery']
        mastery[theme['node_properties']['title']]['val'] = 5
        mastery[theme['node_properties']['title']]['knowledge'] = {}
        for con in theme['node_connections']:
            children = con['nodes_related_son']
            for child in children:
                # mastery[theme['node_properties']['title']]['knowledge'][child['node_properties']['title']]=child['node_properties']['Mastery']
                mastery[theme['node_properties']['title']]['knowledge'][child['node_properties']['title']]=7
    Context['mastery'] = mastery
    # logger.info(Context)
    return render(request, 'teacher/class_info.html', Context)
# Context = {
#     'test_list': ['hi', 'test', '孙志斌'],
#     'stu_info': {
#         '8208181117': {
#             '姓名': '孙志斌',
#             '性别': '男',
#             'hi得分': 0,
#             'test得分': 100.0,
#             '孙志斌得分': 0},
#         '8208181118': {
#             '姓名': '李明',
#             '性别': '男',
#             'hi得分': 0.0,
#             'test得分': 0.0,
#             '孙志斌得分': 0},
#         '8207201920': {
#             '姓名': '谭勋勇',
#             '性别': '女',
#             'hi得分': 0,
#             'test得分': 0,
#             '孙志斌得分': 0}
#     },
#     'mastery': {
#         'Theme1': {
#             'val': 5,
#             'knowledge': {
#                 'Knowledge6': 7,
#                 'Knowledge2': 7,
#                 'Knowledge1': 7}
#         },
#         'Theme2': {
#             'val': 5,
#             'knowledge': {}
#         },
#         'Theme3': {
#             'val': 5,
#             'knowledge': {}
#         },
#         'Theme4': {
#             'val': 5,
#             'knowledge': {}
#         },
#         'Theme6': {
#             'val': 5,
#             'knowledge': {}
#         }
#     }
# }
# 查看单个学生的学习情况
def CheckStuInfo(request):
    # Context记录返回给前端的数据
    Context = {}
    stu_ID = request.GET.get('studentID')
    # stu_ID = '8208181118'
    # 得到学生的基本信息
    stu_info = GetStuBaseInfo(stu_ID)
    Context['stu_info'] = stu_info
    stu_homework_info = GetStuHWInfo(stu_ID)
    Context['stu_homework_info'] = stu_homework_info
    logger.info(Context)
    return render(request, 'teacher/stu_info.html', Context)

# Context = {
#     'stu_info':
#         {'学号': '8208181118',
#          '姓名': '李明',
#          '性别': '男',
#          '班级': '大数据1801',
#          '所做题目个数': 10,
#          '做对题目个数': 8},
#     'stu_homework_info':
#         {'hi':
#              {'做对题目的title': ['Test12', 'Test10'],
#               '做错题目的title': ['Test6'],
#               '得分': 66.66666666666667},
#          "['hi']":
#              {'做对题目的title': ['Test11', 'Test11'],
#               '做错题目的title': [],
#               '得分': 100.0},
#          'test':
#              {'做对题目的title': ['Test4', 'Test7'],
#               '做错题目的title': [],
#               '得分': 100.0}
#          }
# }

# 创建指定内容的作业
def CreateHomework(request):
    # 从前端获取作业的名称，时限和截止日期
    name = request.POST['title']
    timelimit = request.POST['timelimit']
    deadline = request.POST['deadline']
    # 得到题目名称的列表
    title_list = json.loads(request.POST['title_list'])
    # 在all_test文件夹中保存
    logger.info(type(title_list))
    b = {}
    b['title_list'] = title_list
    b = json.dumps(b)
    f2 = open('all_test/' + name + '_' + str(deadline) + '_' + timelimit + '.json', 'w')
    f2.write(b)
    f2.close()
    return redirect('/teacher/')