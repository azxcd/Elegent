#这个文件相当于view进行数据库操作的中间层
import logging
import random
from teacher.models import Knowledge,Theme,Point,Class,Test,Teacher,Student

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Class': Class,
    'Theme': Theme,
    'Knowledge': Knowledge,
    'Point': Point,
    'Test': Test,
    'Teacher':Teacher,
    'Student': Student,
}
FATHER_ENTITIES = {
    'Theme': Class,
    'Knowledge': Theme,
    'Point': Knowledge,
    'Test': Point,
}
logger = logging.getLogger('django')
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
def ResetPassword(username,password):
    user = Student.nodes.get(username=username)
    user.password = password
    user.save()
    return 1
