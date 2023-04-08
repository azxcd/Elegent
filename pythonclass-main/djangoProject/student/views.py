import datetime
import os
import re
import subprocess
import time
import datetime
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
import logging

from .utils import fetch_nodes, add_k_node, add_t_node, create_tests, deleteN, renewN, add_t_connections, GetHWStatus, \
    RenewClass, CreateHomeworkPaper, GetTestNum, get_test_content
import json
from class_login.views import check_login
# 导入用于装饰器修复技术的包
from functools import wraps

logger = logging.getLogger('collect')


def hello_world(request):
    return render(request, 'student/hello_world.html', {})


@check_login
def index(request):
    # 首页用来展示节点的具体数据
    node_details_list = []
    logger.info('开始时间'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # node_details_list.extend(fetch_nodes('Class'))
    # node_details_list.extend(fetch_nodes('Theme'))
    # node_details_list.extend(fetch_nodes('Knowledge'))
    # node_details_list.extend(fetch_nodes('Point'))
    # node_details_list.extend(fetch_nodes('Test'))
    # file = open('./node_details_list.txt', 'w')
    # file.write(str(node_details_list))
    # file.close()
    file = open('./node_details_list.txt', 'r', encoding='utf8')
    node_details_list = eval(file.read())
    file.close()
    logger.info('结束时间'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    return render(request, 'student/index.html', {'searchResult': json.dumps(node_details_list, ensure_ascii=False)})


# 添加题目结点
@check_login
def add_test(request):
    point_list = fetch_nodes('Point')
    p_l = []
    for p in point_list:
        p_l.append(p['node_properties']['title'])
    context = {'point_list': p_l}
    return render(request, 'student/add_test.html', context)
# 函数addTest2Neo用来处理表单提交后服务器响应的结果


def addTest2Neo(request):
    # 首先进行查重的功能，判断
    test_list = fetch_nodes('Test')
    Type = request.POST['Type']
    difficulty = int(request.POST['Difficulty'])
    title = request.POST['title']
    importance = int(request.POST['Importance'])
    teached = int(request.POST['Teached'])
    homeworktimes = int(request.POST['HomeworkTimes'])
    wrongtimes = int(request.POST['WrongTimes'])
    examtimes = int(request.POST['ExamTimes'])
    father = request.POST.getlist('father', '')
    question_text = request.POST['question_text']
    answer_text = request.POST['answer_text']
    for node in test_list:
        if node['node_properties']['attributes']['Content'].replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '') == question_text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''):
            return render(request, 'teacher/wrong.html', {})
    context = {
        'Type': Type, 'difficulty': difficulty, 'title': title,
        'importance': importance, 'father': father,
        'teached': teached, 'homeworktimes': homeworktimes,
        'wrongtimes': wrongtimes, 'examtimes': examtimes,
        'question_text': question_text, 'answer_text': answer_text,
    }
    add_t_node(context)
    return render(request, 'student/hello_world.html', {})


# 学生在这一个模块进行作业的选择
@check_login
def finish_test(request):
    filename = 'all_test/'
    test_list = os.listdir(filename)
    all_test = {}
    #     第一个参数是学生的学号,返回这个学生做过的所有的作业名称
    HW_list = GetHWStatus(request.session['ID'])
    for test_name in test_list:
        l = re.split('[._]', test_name)
        all_test[l[0]] = {}
        all_test[l[0]]['deadline'] = l[1]
        all_test[l[0]]['limittime'] = l[2]
#     status：-1代表未完成，且截止日期已到。0代表未完成，且截止日期未到。1代表已经完成
    status = 0
    # 如果已经完成了作业
    if l[0] in HW_list:
        status = 1
    #     未完成作业
    else:
        # 获得当前日期
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        # 如果截止日期未到
        if datetime.datetime.strptime(l[1], '%Y-%m-%d') > datetime.datetime.strptime(date, '%Y-%m-%d'):
            status = 0
        else:
            status = -1
    all_test[l[0]]['status'] = status
    #     解析一下每一个testname对应的ddl和完成限时
    # 同时需要遍历该学生节点的边，找到学生是否已经完成了相关测试
    Context = {}
    Context['all_test'] = all_test
    # logger.info(Context)
    return render(request, 'student/finish_test.html', Context)


# 返回某一个确定的测试
def certain_test(request):
    # 获取当前作业完成情况
    inputmethod = request.POST['inputmethod']
    # user = request.POST.get('user')
    # 读取前端传给后端的test_name和deadline
    test_name = request.POST['title']
    deadline = request.POST['deadline']
    # 读取前端传给后端的时间限制
    limittime = request.POST['limittime'][0:-3]
    file_name = 'all_test/'+test_name+'_'+deadline+'_'+limittime+'.json'
    if inputmethod == "完成":
        with open(file_name, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
        # 生成json格式的试卷数据
        if list(json_data.keys())[0] == 'title_list':
            logger.info(json_data['title_list'])
            test_context = CreateHomeworkPaper(json_data, test_name)
        else:
            test_context = create_tests(json_data, test_name)
        if len(test_context['code']['Content']) == 0:
            test_context['code']['Number'] = '0'
            # logger.info(test_context['code']['Number'])
        else:
            test_context['code']['Number'] = '1'
            # logger.info(test_context['code']['Number'])
        # 将分钟化成秒存储在limittime中
        test_context['limittime'] = int(limittime)*60
        if test_context['limittime'] == 0:
            test_context['limittime'] -= 1
        test_context['pagetype'] = 'infinish'
    # 如果小测已经完成，则需要显示的是学生做过的题目内容
    else:
        test_context = get_test_content(request.session['ID'], test_name)
        test_context['pagetype'] = 'finish'
        if len(test_context['code']['Content']) == 0:
            test_context['code']['Number'] = '0'
            # logger.info(test_context['code']['Number'])
        else:
            test_context['code']['Number'] = '1'
    test_context['mock'] = 'no'
    return render(request, 'student/check_test.html', test_context)

# 按下提交按钮


def HWSubmit(request):
    test_name = json.loads(request.POST.get('test_name', ''))
    # logger.info(test_name)
    blank_contents = json.loads(request.POST.get('blank_contents', ''))
    blank_answer = json.loads(request.POST.get('blank_answer', ''))
    input_blank = json.loads(request.POST.get('input_blank', ''))
    choice_contents = json.loads(request.POST.get('choice_contents', ''))
    choice_answer = json.loads(request.POST.get('choice_answer', ''))
    input_choice = json.loads(request.POST.get('input_choice', ''))
    code_contents = json.loads(request.POST.get('code_contents', ''))
    code_answer = json.loads(request.POST.get('code_answer', ''))
    input_code = json.loads(request.POST.get('input_code', ''))
    blank_code_contents = json.loads(
        request.POST.get('blank_code_contents', ''))
    blank_code_answer = json.loads(request.POST.get('blank_code_answer', ''))
    input_blank_code = json.loads(request.POST.get('input_blank_code', ''))
    logger.info(input_blank_code)
    # logger.info(request.session['ID'])
    # 记录第几题的对错
    data = {"choice_index": [], "choice_type": [], "blank_index": [], "blank_type": [],
            "code_index": [], "code_type": [], "blank_code_index": [], "blank_code_type": []}
    all_status = {}
    path_1 = "./members/" + request.session['ID']
    folder = os.path.exists(path_1)
    if not folder:  # 判断是否存在学生学号文件夹如果不存在则创建为文件夹
        os.makedirs(path_1)  # makedirs 创建文件时如果路径不存在会创建这个路径
    path_1 = path_1 + '/logger'
    folder = os.path.exists(path_1)
    if not folder:  # 判断是否存在学生学号文件夹如果不存在则创建为文件夹
        os.makedirs(path_1)  # makedirs 创建文件时如果路径不存在会创建这个路径
    # path_1=path_1 + '/' + test_name
    # logger.info(path_1)
    # os.makedirs(path_1)
    # 如果不是模拟题的话，需要记录学生的答题内容
    if test_name != '模拟':
        with open(path_1 + '/' + test_name + '.py', 'w', encoding='utf-8') as fh_1:
            fh_1.write("# 选择题：\n")
            for i in range(len(input_choice)):
                choice_temp = '# 第'+str(i+1)+'题:\n'
                fh_1.write(choice_temp)
                fh_1.write(choice_contents[i]+'\n')
                choice_temp = choice_temp + '# 答案:\n'
                fh_1.write(choice_temp)
                fh_1.write(input_choice[i]+'\n')
            fh_1.write('\n')
            fh_1.write("# 填空题：\n")
            for i in range(len(input_blank)):
                blank_temp = '# 第'+str(i+1)+'题:\n'
                fh_1.write(blank_temp)
                fh_1.write(blank_contents[i]+'\n')
                blank_temp = blank_temp + '# 答案:\n'
                fh_1.write(blank_temp)
                fh_1.write(input_blank[i]+'\n')
            fh_1.write('\n')
            fh_1.write("# 编程题: \n")
            for i in range(len(input_code)):
                code_temp = '# 第'+str(i+1)+'题:\n'
                fh_1.write(code_temp)
                fh_1.write(code_contents[i]+'\n')
                code_temp = code_temp + '# 答案:\n'
                fh_1.write(code_temp)
                fh_1.write(input_code[i]+'\n')
            fh_1.write('\n')
            fh_1.write("# 程序填空题: \n")
            for i in range(len(input_blank_code)):
                blank_code_temp = '# 第' + str(i + 1) + '题:\n'
                fh_1.write(blank_code_temp)
                fh_1.write(blank_code_contents[i] + '\n')
                blank_code_temp = blank_code_temp + '# 答案:\n'
                fh_1.write(blank_code_temp)
                fh_1.write(input_blank_code[i] + '\n')
    # 选择题核对答案
    for i in range(len(input_choice)):
        data['choice_index'].append(str(i + 1))
        if choice_answer[i].strip() == input_choice[i]:
            # 1代表做对了
            data['choice_type'].append('1')
            # add_t_connections(contents[i])
            # 在学生节点和题目节点之间创建连接,通过session来获取学生学号并进行参数的传递
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], choice_contents[i], test_name, '1', input_choice[i])
                all_status[choice_contents[i]] = 1
            # logger.info('ture')
        else:
            # logger.info('wrong')
            data['choice_type'].append('0')
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], choice_contents[i], test_name, '0', input_choice[i])
                all_status[choice_contents[i]] = 0
    # 填空题核对答案
    for i in range(len(input_blank)):
        data['blank_index'].append(str(i + 1))
        if blank_answer[i].strip().replace(" ", "") == input_blank[i].replace(" ", ""):
            data['blank_type'].append('1')
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], blank_contents[i], test_name, '1', input_blank[i])
                all_status[blank_contents[i]] = 1
        else:
            data['blank_type'].append('0')
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], blank_contents[i], test_name, '0', input_blank[i])
                all_status[blank_contents[i]] = 0
    # 程序填空题核对答案
    for i in range(len(input_blank_code)):
        # 记录blank_code的第几题
        data['blank_code_index'].append(str(i + 1))
        # 判断这个学生是否在members中有文件夹
        path = "./members/" + request.session['ID']
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        flag = '1'
        # 放入runblank_code.py文件夹中
        with open(path + '/runblank_code.py', 'w', encoding='utf8') as fh:
            fh.write('#coding=utf-8' + '\n' + input_blank_code[i])
        import sys
        sys.path.append(path)
        try:
            result = subprocess.check_output(["python3", path + "/runblank_code.py"], shell=False,
                                             stderr=subprocess.STDOUT)
            result = result.decode("utf-8")
            # 将path拿走
            sys.path.remove(path)
        # 发生了异常
        except:
            sys.path.remove(path)
            logger.info('except')
            flag = '0'
        #     没有发生异常的话
        else:
            logger.info(blank_code_answer)
            if result != blank_code_answer[i]:
                flag = '0'

        # 判断题目的对错
        if flag == '1':
            data['blank_code_type'].append('1')
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], blank_code_contents[i], test_name, '1', input_blank_code[i])
                all_status[blank_code_contents[i]] = 1
        else:
            data['blank_code_type'].append('0')
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], blank_code_contents[i], test_name, '0', input_blank_code[i])
                all_status[blank_code_contents[i]] = 0
    # 编程题核对答案,因为编程题在运行过程中难免会出错，所以需要使用try语句
    # input_code是编程题的答案列表
    # logger.info(code_answer)
    if test_name != "模拟":
        for i in range(len(input_code)):
            logger.info(code_answer[i])
            data['code_index'].append(str(i+1))
            flag = '1'
            # 用function.py这个文件运行代码
            # logger.info("写入function文件")
            path = "./members/" + request.session['ID']
            # logger.info(path)
            folder = os.path.exists(path)
            if not folder:  # 判断是否存在学生学号文件夹如果不存在则创建为文件夹
                os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            # 用function.py这个文件运行代码
            l = len(os.listdir(path))
            # logger.info(l)
            # 创建存放function的文件夹
            path = path+'/function_'+str(l)
            os.makedirs(path)
            # logger.info(path)
            # 每一个学生的文件夹中有一个叫function的，用于存储当前运行按钮对应的代码
            with open(path + '/function.py', 'w', encoding='utf8') as fh:
                fh.write(input_code[i])
            import sys
            # logger.info(path)
            sys.path.append(path)
            # 阿里云用python3，本地用python
            stmt = 'python3 tmp_submit.py' + ' ' + \
                request.session['ID']+' ' + \
                str(l)+' '+test_name+' '+code_answer[i]
            # result = subprocess.check_output(stmt)
            try:
                # 运行stmt命令
                result = subprocess.check_output(stmt, shell=True)
                # from function import fact
                # logger.info(sys.path)
                # 将path拿走
                sys.path.remove(path)
                # logger.info(result.decode()[0])
            # 发生了异常
            except:
                sys.path.remove(path)
                flag = '0'
            #     没有发生异常的话
            else:
                # logger.info(result)
                flag = result.decode()[0]
            # flag为1代表正确，0代表错误
            data['code_type'].append(flag)
            # logger.info(flag)
            if test_name != "模拟":
                add_t_connections(
                    request.session['ID'], code_contents[i], test_name, flag, input_code[i])
            if flag == '1':
                all_status[code_contents[i]] = 1
            else:
                all_status[code_contents[i]] = 0
    # 利用all_status更新知识节点的属性
    if test_name != "模拟":
        RenewClass(all_status)
    # 记录学生做模拟题的次数和时间
    if test_name == '模拟':
        t = time.strftime('%H:%M:%S', time.localtime())
        today = datetime.date.today()
        formatted_today = today.strftime('date_%y_%m_%d')
        filename = './mock_times/' + formatted_today + '.csv'
        if not os.path.exists(filename):
            with open(filename, 'w') as file_object:
                file_object.write("状态,学号,时间,姓名,本次题目数量,知识点和对应题目数量,做对题目数量\n")
        username = request.session['ID']
        name = request.session['name']
        state = '2'
        nums = str(len(data['choice_index']) +
                   len(data['blank_index'])+len(data['code_index']))
        points_nums_str = '0'
        right_num = str(data['choice_type'].count(
            '1')+data['blank_type'].count('1')+data['code_type'].count('1'))
        with open(filename, 'a') as object:
            object.write(str(state) + ',' + username + ',' + t + ',' + name + ',' +
                         nums + ',' + points_nums_str + ',' + right_num+'\n')
    ret = {"status": True, "errmsg": None, "data": data}
    return HttpResponse(json.dumps(ret))
# 运行按钮编程题核对答案


def runcode(request):
    # logger.info("enter check_code")
    testname = json.loads(request.POST.get('test_name', ''))
    logger.info(testname)
    logger.info(request.session['ID'])
    contents = json.loads(request.POST.get('test_text', ''))
    answer = request.POST.get('answer_text', '')
    logger.info(answer)
    code = request.POST.get('code_text', '')
    # logger.info(testname)
    # 判断这个学生是否在members中有文件夹
    path = "./members/"+request.session['ID']
    # logger.info(path)
    folder = os.path.exists(path)
    # logger.info(folder)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        # logger.info("创建新文件夹")
    flag = '1'
    # logger.info(path)
    # 每一个学生的文件夹中有一个叫function的，用于存储当前运行按钮对应的代码
    with open(path+'/function.py', 'w', encoding='utf8') as fh:
        fh.write(code)
    import sys
    # logger.info(path)
    sys.path.append(path)
    # logger.info(sys.path)
    # 直接运行这个判断的脚本
    # sys.path.append('/home/sun/usr/local/python_projects/python_web/PythonClass')
    # 把作业名称放进去用以区分
    stmt = 'python3 tmp_function.py'+' ' + \
        request.session['ID']+' '+testname+' '+answer
    try:
        logger.info('try1')
        result = subprocess.check_output(stmt, shell=True)
        # from function import fact
        logger.info(result.decode())
        # 将path拿走
        sys.path.remove(path)
        # logger.info(result.decode()[0])
    # 发生了异常
    except:
        sys.path.remove(path)
        logger.info('except')
        flag = '0'
    #     没有发生异常的话
    else:
        flag = result.decode()[0]

    # logger.info(result.decode()[0])
    # flag为1代表正确，0代表编译错误，2代表结果出错
    logger.info(flag)
    ret = {"status": True, "errmsg": None, "data": flag}
    return HttpResponse(json.dumps(ret))

# 运行按钮程序填空题核对答案


def runblank_code(request):
    # logger.info("enter check_code")
    testname = json.loads(request.POST.get('test_name', ''))
    contents = json.loads(request.POST.get('test_text', ''))
    answer = request.POST.get('answer_text', '')
    blank_code_text = request.POST.get('blank_code_text', '')
    # 判断这个学生是否在members中有文件夹
    path = "./members/"+request.session['ID']
    # logger.info(path)
    folder = os.path.exists(path)
    # logger.info(folder)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        # logger.info("创建新文件夹")
    flag = '1'
    # logger.info(path)
    # 每一个学生的文件夹中有一个叫runblank_code的，用于存储当前运行按钮对应的代码
    with open(path+'/runblank_code.py', 'w', encoding='utf8') as fh:
        fh.write('#coding=utf-8'+'\n'+blank_code_text)
    import sys
    # # logger.info(path)
    sys.path.append(path)
    logger.info(sys.path)
    # # 直接运行这个判断的脚本
    # # 把作业名称放进去用以区分
    # stmt = 'python3 tmp_function.py'+' '+request.session['ID']+' '+testname+' '+answer
    try:
        logger.info('try1')
        result = subprocess.check_output(
            ["python3", path+"/runblank_code.py"], shell=False, stderr=subprocess.STDOUT)
        result = result.decode("utf-8")
        logger.info(result)
        # 将path拿走
        sys.path.remove(path)
    # 发生了异常
    except:
        sys.path.remove(path)
        logger.info('except')
        flag = '0'
    #     没有发生异常的话
    else:
        logger.info(result)
        logger.info(answer)
        if result != answer:
            flag = '2'

    # # flag为1代表正确，0代表编译错误，2代表结果出错
    logger.info(flag)
    ret = {"status": True, "errmsg": None, "data": flag}
    return HttpResponse(json.dumps(ret))

# 模拟测试模块


@check_login
def mock_test(request):
    node_details_list = []
    node_details_list.extend(fetch_nodes('Class'))
    node_details_list.extend(fetch_nodes('Theme'))
    node_details_list.extend(fetch_nodes('Knowledge'))
    node_details_list.extend(fetch_nodes('Point'))
    node_details_list.extend(fetch_nodes('Test'))
    return render(request, 'student/mock_test.html', {'searchResult': json.dumps(node_details_list, ensure_ascii=False)})

# 生成模拟


def create_mock(request):
    # 得到对应的内容（test的节点名称和对应的出题数目）
    point_nums = request.POST.getlist('nums', '')
    points = request.POST.getlist('node_name', '')
    # 获取当前时间以标识卷子
    # current_time = datetime.datetime.now()
    # logger.info(current_time)
    num_sum = 0
    point_nums_str = ''
    test_dict = {}
    for i in range(len(points)):
        num = int(point_nums[i])
        num_sum += num
        point_nums_str += points[i] + ':' + str(num) + '、'
        if test_dict.__contains__(points[i]):
            test_dict[points[i]] = test_dict[points[i]] + num
        else:
            test_dict[points[i]] = num
    # logger = logging.getLogger('django')
    # logger.info(test_dict)
    # context是输入，里面的test_dict是字典，包含每个知识点的希望出题的数目。
    context = {'test_dict': test_dict}
    # 将内容保存为json
    # b = json.dumps(context)
    # f2 = open('all_test/' + str(current_time) + '.json', 'w')
    # f2.write(b)
    # f2.close()
    # test_context也是一个字典，应该是{’choice‘:{'Content':[],'Answer':[]},’blank‘:{'Content':[],'Answer':[]},’code‘:{'Content':[],'Answer':[]}}
    test_context = create_tests(context, "模拟")
    test_context['limittime'] = -1
    # logger.info()
    test_context['pagetype'] = 'infinish'
    test_context['mock'] = 'yes'
    logger.info(test_context)
    # 记录学生做模拟的时间
    t = time.strftime('%H:%M:%S', time.localtime())
    today = datetime.date.today()
    formatted_today = today.strftime('date_%y_%m_%d')
    filename = './mock_times/' + formatted_today + '.csv'
    if not os.path.exists(filename):
        with open(filename, 'w') as file_object:
            file_object.write("状态,学号,时间,姓名,本次题目数量,知识点和对应题目数量,做对题目数量\n")
    # 在session中记录学生的id和姓名
    state = 1
    username = request.session["ID"]
    name = request.session["name"]

    with open(filename, 'a') as object:
        object.write(
            str(state) + ',' + username + ',' + t + ',' + name + ',' + str(num_sum) + ',' + point_nums_str + ',' + str(
                0) + '\n')
    return render(request, 'student/check_test.html', test_context)


def FindTest(request):
    point_name = request.POST['point_name']
    # logger.info(point_name)
    test_num = GetTestNum(point_name)
    ret = {"status": True, "errmsg": None,
           "data": test_num, "node_name": point_name}
    return HttpResponse(json.dumps(ret))
