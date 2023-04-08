from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipFrom,
    RelationshipTo,
    IntegerProperty, UniqueIdProperty,
)
#章
from .nodeutils import NodeUtils

class Theme(StructuredNode, NodeUtils):
    type = 'Theme'
    # 每一章的名称
    title = StringProperty()
    # 每一章的难度
    Difficulty = IntegerProperty()
    # 每一章的重要程度
    Importance = IntegerProperty()
    # 每一章的班级掌握程度
    Mastery = IntegerProperty()
    # test_right_num/test_num*10就是Mastery
    # 题目子节点被做的次数
    test_num = IntegerProperty()
    # 题目子节点被做对的次数
    test_right_num = IntegerProperty()
    # 每一章在教学大纲中的权重
    Weights = IntegerProperty()
    # 是否已经讲解,0代表没有讲解,1代表已经讲解
    Teached = IntegerProperty()
    uid = UniqueIdProperty(primary_key=True)
    # 下面这个属性用于生成关系，指向父节点
    relation_from = RelationshipFrom('.Class.Class','include')
    relation_to = RelationshipTo('.Knowledge.Knowledge', 'include')
    # serialize可以返回数据
    @property
    def serialize(self):
        return {
            'node_properties': {
                'type' : self.type,
                'title': self.title,
                'uid': self.uid,
                'attributes':{
                    'Difficulty': self.Difficulty,
                    'Importance': self.Importance,
                    'Mastery': self.Mastery,
                    'Weights': self.Weights,
                    'Teached': self.Teached,
                }
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Class',
                'nodes_related': self.serialize_relationships(self.relation_from.all()),
                'nodes_type_son': 'Knowledge',
                'nodes_related_son': self.serialize_relationships(self.relation_to.all()),
            },
        ]