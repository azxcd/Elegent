from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipFrom,
    RelationshipTo,
    IntegerProperty,
    UniqueIdProperty,
)

from .RelFinish import RelFinish
from .nodeutils import NodeUtils


class Student(StructuredNode, NodeUtils):
    type = 'Student'
    # 学号
    username = StringProperty()
    password = StringProperty()
    name = StringProperty()
    # 性别
    gender = IntegerProperty()
    #班级
    study_class = StringProperty()
    # #总共做了多少次小测
    # practice_number = StringProperty()
    # #每次小测的评分
    # practice_grade_1 = StringProperty()
    # 学生分类:0000Python代表是测试人员的账号
    stu_classify = StringProperty()
    #总共做了多少题
    test_num = IntegerProperty()
    #错对多少题
    test_right_num = IntegerProperty()

    uid = UniqueIdProperty(primary_key=True)

    # 和题目的关系
    relation_to = RelationshipTo('.Test.Test', 'finish',model=RelFinish)

    # serialize可以返回数据
    @property
    def serialize(self):
        return {
            'node_properties': {
                'type' : self.type,
                'username':self.username,
                'password':self.password,
                'name':self.name,
                'gender':self.gender,
                'study_class':self.study_class,
                'uid': self.uid,
                'test_num': self.test_num,
                'test_right_num': self.test_right_num,
                'stu_classify':self.stu_classify,
            },
        }

    @property
    def serialize_connections(self):
        return [
           {
               'nodes_type_son': 'Test',
               'nodes_related_son': self.serialize_relationships(self.relation_to.all()),
           },
        ]