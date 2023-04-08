import logging
import random
#与数据库交互的函数
from .models import Knowledge,Theme,Point,Class,Test,Student
from .constants import  fetch_tests, fetch_points, fetch_node, deleteNode, renewNode, renewTestNode

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
# 获取某个类型的所有节点，以字典形式返回
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
                                              Teached = node_info['teached'],
                                              test_num = 0,
                                              test_right_num = 0,)
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

# 出题
def create_tests(info):
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
    context = {'choice':{'Content':[],'Answer':[]},'blank':{'Content':[],'Answer':[]},'code':{'Content':[],'Answer':[]}}
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

#返回存储所有节点的title的一个列表
def fetch_all_nodes_title():
    #获取所有的节点名称
    class_list = fetch_nodes('Class')
    theme_list = fetch_nodes('Theme')
    knowledge_list = fetch_nodes('Knowledge')
    point_list = fetch_nodes('Point')
    test_list = fetch_nodes('Test')
    all_l = []
    for p in point_list:
        all_l.append(p['node_properties']['title'])
    for k in knowledge_list:
        all_l.append(k['node_properties']['title'])
    for t in theme_list:
        all_l.append(t['node_properties']['title'])
    for c in class_list:
        all_l.append(c['node_properties']['title'])
    for c in test_list:
        all_l.append(c['node_properties']['title'])
    return all_l


# 删除节点
def deleteN(title):
    deleteNode(title)

#更新节点
def renewN(title,Difficulty,Importance,Weights,Teached):
    renewNode(title,Difficulty,Importance,Weights,Teached)


# 更新题目节点
def renewTestN(title,testtype,Difficulty,Importance,Teached,testanswer,testcontent):
    renewTestNode(title,testtype,Difficulty,Importance,Teached,testanswer,testcontent)

# 得到testname作业中每个学生的得分情况
def CheckStu(testname):
    # 记录每个题目的做题信息
    test_list= {}
    # 记录学生分数
    df_stu = {}

    stu_list = Student.nodes
    # 计算每个学生的得分
    for stu in stu_list:
        # if stu.stu_classify=='0000Python':
        #     continue
        # logger.info(stu.name)
        # 首先赋值为0分
        score=0
        # 为每个学生记录题目数量和正确题目数量
        num=0
        right_num=0
        # 遍历可以得到和stu学生相关的题目分别是什么
        for test_finish in stu.relation_to:
            # 得到学生和题目之间的关系
            rel = stu.relation_to.relationship(test_finish)
            # 如果这条边的title是testname
            if rel.title==testname:
                # 这个学生的记录题目加一
                num=num+1
                # 找到题目的title，查看是否在test_list中
                title = test_finish.title
                # 如果不在test_list中，就新建一个dict的项
                if test_finish.title not in test_list.keys():
                    test_list[title]={}
                    test_list[title]['内容'] = test_finish.Content
                    test_list[title]['答案'] = test_finish.Answer
                    test_list[title]['正确人数'] = 0
                    test_list[title]['错误人数'] = 0
                if rel.correct=='1':
                    test_list[title]['正确人数']+=1
                    right_num=right_num+1
                else:
                    test_list[title]['错误人数'] += 1
            # 计算真实得分
        if num != 0:
            score = int(right_num * 100 / num)
        # 记录得分
        df_stu[stu.name]=score
    return (df_stu,test_list)

# 得到每个学生的作业得分情况,参数是所有作业名称的list
def GetStuInfo(tests_list):
    # logger.info(tests_list)
    # 记录学生的学习信息
    stu_info = {}
    stu_list = Student.nodes
    # 遍历学生节点
    for stu in stu_list:
        if stu.stu_classify=='0000Python':
            continue
        info={}
        info['姓名'] = stu.name
        if stu.gender==1:
            info['性别'] = '男'
        else:
            info['性别'] = '女'
        #     遍历每一次作业名称
        for testname in tests_list:
            # 初始设置得分是0
            score=0
            # 为每个学生记录题目数量和正确题目数量
            num = 0
            right_num = 0
            # 遍历可以得到和stu学生相关的题目分别是什么
            for test_finish in stu.relation_to:
                # 得到学生和题目之间的关系
                rel = stu.relation_to.relationship(test_finish)
                # 如果这条边的title是testname
                if rel.title == testname:
                    # 这个学生的记录题目加一
                    num = num + 1
                    # 该题目做对了
                    if rel.correct == '1':
                        right_num = right_num + 1
                # 计算真实得分
            if num != 0:
                score = int(right_num * 100 / num)
            #     记录得分
            info[testname+'得分']=score
        # 用学生的学号作为key
        stu_info[stu.username]=info
        # logger.info(stu_info)
    return stu_info

# 得到某个学生节点的基本型信息
def GetStuBaseInfo(stu_id):
    stu_info = {}
    stu = Student.nodes.get(username=stu_id)
    # 存储该学生的基本信息
    stu_info['学号'] = stu.username
    stu_info['姓名'] = stu.name
    if stu.gender == 1:
        stu_info['性别'] = '男'
    else:
        stu_info['性别'] = '女'
    stu_info['班级'] = stu.study_class
    stu_info['所做题目个数'] = stu.test_num
    stu_info['做对题目个数'] = stu.test_right_num
    return stu_info

# 获得某个学生的所有作业的信息
def GetStuHWInfo(stu_id):
    # 得到学生节点
    stu = Student.nodes.get(username=stu_id)
    stu_homework_info = {}
    # 遍历可以得到和stu学生相关的题目分别是什么
    for test_finish in stu.relation_to:
        # 得到学生和题目之间的关系
        rel = stu.relation_to.relationship(test_finish)
#         判断这个关系对应的作业名称是否在stu_homework_info中
        if rel.title not in stu_homework_info.keys():
            stu_homework_info[rel.title]={}
            stu_homework_info[rel.title]['做对题目的title'] = []
            stu_homework_info[rel.title]['做错题目的title'] = []
        # 如果题目做对了
        if rel.correct == '1':
            stu_homework_info[rel.title]['做对题目的title'].append(test_finish.title)
        else:
            stu_homework_info[rel.title]['做错题目的title'].append(test_finish.title)
#     最后遍历stu_homeWork_info中的每一项，计算每个作业的得分
    for key in stu_homework_info.keys():
        stu_homework_info[key]['得分'] = 100*len(stu_homework_info[key]['做对题目的title'])/(len(stu_homework_info[key]['做对题目的title'])+len(stu_homework_info[key]['做错题目的title']))
    return stu_homework_info
