import logging
import random

from teacher.models import Knowledge, Theme, Point, Class, Test, Student
from .constants import  fetch_tests, fetch_points, fetch_node, deleteNode, renewNode

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Class': Class,
    'Theme': Theme,
    'Knowledge': Knowledge,
    'Point': Point,
    'Test': Test,
}
FATHER_ENTITIES = {
    'Theme': Class,
    'Knowledge': Theme,
    'Point': Knowledge,
    'Test': Point,
}
logger = logging.getLogger('collect')
# 获取某个类型的所有节点
def fetch_nodes(node_type):
    node_list = MODEL_ENTITIES[node_type].nodes
    node_detail_list = []
    for node in node_list:
        node_details = node.serialize
        node_details['node_connections'] = []
        if (hasattr(node, 'serialize_connections')):
            node_details['node_connections'] = node.serialize_connections
        node_detail_list.append(node_details)
    return node_detail_list
# 添加知识节点
def add_k_node(node_info):
    # 录入该节点的基本信息
    # node  = MODEL_ENTITIES[node_info['type']](Difficulty=int(node_info['difficulty']),Importance=int(node_info['importance']),title = node_info['title'])
    node  = MODEL_ENTITIES[node_info['type']](Difficulty=node_info['difficulty'],
                                              Importance=node_info['importance'],
                                              title = node_info['title'],
                                              Weights = node_info['weights'],
                                              Mastery = node_info['mastery'],
                                              Teached = node_info['teached'])
    # 创造该节点
    node.save()
    # 找到该节点的父节点
    father = FATHER_ENTITIES[node_info['type']].nodes.get(title=node_info['father'])
    node.relation_from.connect(father)
# 添加题目节点
def add_t_node(test_info):
    node = Test(Difficulty=test_info['difficulty'],Importance=test_info['importance'],
                title = test_info['title'],WrongTimes = test_info['wrongtimes'],
                HomeworkTimes = test_info['homeworktimes'],ExamTimes = test_info['examtimes'],
                Teached = test_info['teached']
                )
    node.Type = test_info['Type']
    node.Answer = test_info['answer_text']
    node.Content = test_info['question_text']
    node.save()
    father_list = test_info['father']
    # logger.info(father_list)
    for father in father_list:
        father_node = Point.nodes.get(title=father)
        node.relation_from_point.connect(father_node)

# 出题,第一个参数是小测中的类型个数，第二个参数是本次小测的名称
def create_tests(info,test_name):
    test_dict = info['test_dict']
    points =list(test_dict.keys())
    # 答案列表
    answer_list = []
    # 题目索引列表用于判断题目是否被出过了
    test_list = []
    # 这个list可以记录每一个题目
    content_list = []
    # 类型对应字典
    type_dict = {'1':'choice','2':'blank','3':'code'}
    # 返回值
    context = {'choice':{'Content':[],'Answer':[]},'blank':{'Content':[],'Answer':[]},'code':{'Content':[],'Answer':[], 'Number':'0'},

               'testname':{'Name':[test_name]}}
    # 开始出题
    for p in points:
        if test_dict[p]<1:
            continue
            # 找到和这个point关联的所有的test
        test_nodes = fetch_tests(p)
        # 出p个题
        test_nodes = random.sample(test_nodes, test_dict[p])
        for node in test_nodes:
            if node['title'] in test_list:
                temp_list = fetch_tests(p)
                temp_list = random.choice(temp_list)
                test_nodes.append(temp_list)
            if node['title'] not in test_list:
                # logger.info(type(node['Type']))
                t = type_dict[str(node['Type'])]
                # logger.info(t)
                context[t]['Content'].append(node['Content'])
                context[t]['Answer'].append(node['Answer'])
                test_list.append(node['title'])
                relate_nodes = fetch_points(node['title'])
                for rnode in relate_nodes:
                    if rnode['title'] in points:
                        test_dict[rnode['title']] -= 1
    return context

# 根据教师的要求创建作业
def CreateHomeworkPaper(data, test_name):
    test_list = data['title_list']
    # logger.info(test_list)
    context = {'choice': {'Content': [], 'Answer': []},
               'blank': {'Content': [], 'Answer': []},
               'code': {'Content': [], 'Answer': [], 'Number': '0'},
               'blank_code': {'Content': [], 'Answer': [], 'Number': '0'},
               'testname': {'Name': [test_name]}}
    # 遍历题目名称
    for t in test_list:
        test = Test.nodes.get(title=t)
        logger.info(test)
        if test.Type=='1':
            context['choice']['Content'].append(test.Content)
            context['choice']['Answer'].append(test.Answer)
        if test.Type=='2':
            context['blank']['Content'].append(test.Content)
            context['blank']['Answer'].append(test.Answer)
        if test.Type=='3':
            context['code']['Content'].append(test.Content)
            context['code']['Answer'].append(test.Answer)
        if test.Type == '4':
            context['blank_code']['Content'].append(test.Content)
            context['blank_code']['Answer'].append(test.Answer)
    return context



# 获取学生做过的某个试卷内容
def get_test_content(stu_id, test_name):
    # 得到学生节点
    stu = Student.nodes.get(username=stu_id)
    # test节点类型对应字典
    type_dict = {'1': 'choice', '2': 'blank', '3': 'code','4':'blank_code'}
    # 返回值
    context = {'choice': {'Content': [], 'Answer': []}, 'blank': {'Content': [], 'Answer': []},
               'code': {'Content': [], 'Answer': [], 'Number': '0'},
               'blank_code': {'Content': [], 'Answer': [], 'Number': '0'},
               'testname': {'Name': [test_name]},
               'score': {}}
    # 遍历可以得到和stu学生相关的当前小测的题目分别是什么
    score_cor = 0
    score_err = 0
    for test_finish in stu.relation_to:
        # 得到学生和题目之间的边
        rel = stu.relation_to.relationship(test_finish)
        # 如果边代表的小测对应当前小测名
        if rel.title == test_name:
            if rel.correct == '1':
                score_cor += 1
            else:
                score_err += 1
            # logger.info("rel:"+rel.correct)
            # 将题目加入context中
            t = type_dict[str(test_finish.Type)]
            content_correct = {}
            content_correct['Content'] = test_finish.Content
            content_correct['Correct'] = rel.correct
            content_correct['Record'] = rel.input_context
            context[t]['Content'].append(content_correct)
            context[t]['Answer'].append(test_finish.Answer)
    context['score']['Correct'] = str(score_cor)
    context['score']['Error'] = str(score_err)
    return context

# 删除节点
def deleteN(title):
    deleteNode(title)

#更新节点
def renewN(title,Difficulty,Importance):
    renewNode(title,Difficulty,Importance)
# 得到特定point下有多少个test
def GetTestNum(point_name):
    p = Point.nodes.get(title = point_name)
    return len(p.relation_to)

# 添加做题的关系，ID是学生的学号，content是题目内容，name是本次测试的名字，a代表题目是否做对1代表做对，0代表做错,input_context是学生的作题答案
def add_t_connections(ID, content, name, a,input_context):
# def add_t_connections(content):
#     logger.info('add_t_connections')
    # father_list = fetch_nodes('Student')
    test_list = fetch_nodes('Test')
    # logger.info(content)
    # 先找到题目节点
    for node in test_list:
        if node['node_properties']['attributes']['Content'].replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '') == content.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''):
            # logger.info('found_test')
            # logger.info(node)
            # 再找到父节点学生节点
            father_node = Student.nodes.get(username=ID)
            # logger.info(type(father_node))
            # 在真正的场景下是使用uid进行检索的，但是在测试的数据库中有的题目没有uid这个属性，所以先用title
            test_node = Test.nodes.get(title=node['node_properties']['title'])
            # test_node = Test.nodes.get(uid=node['node_properties']['uid'])
            # logger.info(type(test_node))
            # Test和Student节点建立边的联系
            test_node.relation_from_student.connect(father_node, {'title': name, 'correct': a,'input_context':input_context})


# 得到这个学生做过的所有的作业的名称
def GetHWStatus(stu_id):
    HWList = {}
    stu = Student.nodes.get(username=stu_id)
    # 遍历可以得到和stu学生相关的题目分别是什么
    for test_finish in stu.relation_to:
        # 得到学生和题目之间的关系
        rel = stu.relation_to.relationship(test_finish)
        HWList[rel.title]=1
    HWList = HWList.keys()
    return HWList
# 更新知识节点的对错次数和班级掌握程度
def RenewClass(all_status):
    for key,value in all_status.items():
        test = Test.nodes.get(Content=key)
        # 首先更改test之上的Point节点的内容
        for p in test.relation_from_point:
            p.test_num+=1
            p.test_right_num+=value
            p.Weights = int(round(p.test_right_num/p.test_num,1)*10)
            # 更改Point之上的Knowledge节点的内容
            for k in p.relation_from:
                k.test_num += 1
                k.test_right_num += value
                k.Weights = int(round(k.test_right_num / k.test_num, 1) * 10)
                # 更改Knowledge之上的Theme节点的内容
                for t in k.relation_from:
                    t.test_num += 1
                    t.test_right_num += value
                    t.Weights = int(round(k.test_right_num / k.test_num, 1) * 10)
    # logger.info(all_status)

