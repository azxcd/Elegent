from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    IntegerProperty,
    UniqueIdProperty,
)
#课程
from .nodeutils import NodeUtils

# 重要的属性是title,id和type
class Class(StructuredNode, NodeUtils):
    type = 'Class'
    title = StringProperty()
    Teacher = StringProperty()
    uid = UniqueIdProperty(primary_key=True)
    # id= IntegerProperty(index=True)
    relation_to = RelationshipTo('.Theme.Theme','include')
    # serialize可以返回数据
    @property
    def serialize(self):
        return {
            'node_properties': {
                'type' : self.type,
                'title': self.title,
                'uid': self.uid,
                'attributes':{
                    'Teacher': self.Teacher,
                }
            },
        }
    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type_son': 'Theme',
                'nodes_related_son': self.serialize_relationships(self.relation_to.all()),
            },
    ]