from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    IntegerProperty,
    UniqueIdProperty,
)

from .nodeutils import NodeUtils


class Teacher(StructuredNode, NodeUtils):
    type = 'Teacher'
    username = StringProperty()
    password = StringProperty()
    uid = UniqueIdProperty(primary_key=True)

    # id= IntegerProperty(index=True)
    # themes = RelationshipTo('.Theme.Theme','include')
    # serialize可以返回数据
    @property
    def serialize(self):
        return {
            'node_properties': {
                'type': self.type,
                'username': self.username,
                'password': self.password,
                'uid': self.uid,
            },
        }
    # 对边进行序列化
    @property
    def serialize_connections(self):
        return [
            # {
            #     'nodes_type': 'Theme',
            #     'nodes_related': self.serialize_relationships(self.themes.all()),
            # },
        ]