from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipFrom,
    IntegerProperty,
    RelationshipTo, UniqueIdProperty,
)
#节
from .nodeutils import NodeUtils

class Knowledge(StructuredNode, NodeUtils):
    type = 'Knowledge'
    title = StringProperty()
    Difficulty = IntegerProperty()
    Importance = IntegerProperty()
    Mastery = IntegerProperty()
    # test_right_num/test_num*10就是Mastery
    # 题目子节点被做的次数
    test_num = IntegerProperty()
    # 题目子节点被做对的次数
    test_right_num = IntegerProperty()
    Weights = IntegerProperty()
    Teached = IntegerProperty()
    uid = UniqueIdProperty(primary_key=True)
    # id= IntegerProperty(index=True)
    # 下面这两个属性用于生成关系
    relation_from = RelationshipFrom('.Theme.Theme', 'include')
    relation_to = RelationshipTo('.Point.Point', 'include')

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
                    'Mastery':self.Mastery,
                    'Weights':self.Weights,
                    'Teached':self.Teached,
                }
            },
        }
    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Theme',
                'nodes_related': self.serialize_relationships(self.relation_from.all()),
                'nodes_type_son': 'Point',
                'nodes_related_son': self.serialize_relationships(self.relation_to.all()),
            },
    ]
