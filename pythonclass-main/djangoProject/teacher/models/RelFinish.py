from neomodel import (
    StringProperty,
    UniqueIdProperty,
    StructuredRel,
)
from .nodeutils import NodeUtils
# 学生节点和题目节点之间的关系类
class RelFinish(StructuredRel):
    # 当前小测名称
    title = StringProperty()
    # 是否做对
    correct = StringProperty()
    uid = StringProperty()
    # 学生输入的答案
    input_context = StringProperty()

    def serialize(self):
        return {
            'relation_properties': {
                'input_context': self.input_context,
                'title': self.title,
                'correct': self.correct,
                'uid': self.uid,
            },
        }

    # def serialize_connections(self):
    #     return [
    #         # {
    #         #     'nodes_type': 'Theme',
    #         #     'nodes_related': self.serialize_relationships(self.relation.all()),
    #         # },
    #     ]

