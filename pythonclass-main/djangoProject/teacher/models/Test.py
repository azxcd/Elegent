from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipFrom,
    IntegerProperty,
    UniqueIdProperty,
)
from .RelFinish import RelFinish
from .nodeutils import NodeUtils

class Test(StructuredNode, NodeUtils):
    type = 'Test'
    title = StringProperty()
    Type = StringProperty()
    Importance= IntegerProperty()
    Difficulty = IntegerProperty()
    Answer = StringProperty()
    Content = StringProperty()
    HomeworkTimes = IntegerProperty()
    WrongTimes = IntegerProperty()
    ExamTimes = IntegerProperty()
    Teached = IntegerProperty()
    uid = UniqueIdProperty(primary_key=True)
    # 用于生成关系
    relation_from_point = RelationshipFrom('.Point.Point', 'relate')
    # 学生与题目的关系
    relation_from_student = RelationshipFrom('.Student.Student', 'finish',model=RelFinish)
    # serialize可以返回数据
    @property
    def serialize(self):
        return {
            'node_properties': {
                'type' : self.type,
                'title': self.title,
                'Type':self.Type,
                'uid': self.uid,
                'attributes':{
                    'Importance': self.Importance,
                    'Difficulty': self.Difficulty,
                    'HomeworkTimes':self.HomeworkTimes,
                    'WrongTimes':self.WrongTimes,
                    'ExamTimes':self.ExamTimes,
                    'Teached':self.Teached,
                    'Answer': self.Answer,
                    'Content': self.Content,
                }
            },
        }
    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Point',
                'nodes_related': self.serialize_relationships(self.relation_from_point.all()),
                'nodes_type_2': 'Student',
                'nodes_related_2': self.serialize_relationships(self.relation_from_student.all()),
            },
        ]