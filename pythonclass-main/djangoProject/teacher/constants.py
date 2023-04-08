from neomodel import db

# countries = db.cypher_query(
#     '''
#     match (s:Point{p}) with s match (s)-[re]->(t) return t
#     '''.format(p='{title:\''+'Point3'+'\'}')
# )[0]

def fetch_tests(point_name):
    tests = db.cypher_query(
    '''
    match (s:Point{p}) with s match (s)-[re]->(t) return t
    '''.format(p='{title:\''+point_name+'\'}')
    )[0]
    return [test[0] for test in tests]

def fetch_points(test_name):
    points = db.cypher_query(
    '''
    match (s:Point{p}) with s match (s)-[re]->(t) return t
    '''.format(p='{title:\''+test_name+'\'}')
    )[0]
    return [point[0] for point in points]
# 找到特定名字的node
def fetch_node(node_name):
    points = db.cypher_query(
        '''
        Match (n) where n.title='{p}' return n
        '''.format(p=node_name)
    )[0]
    return [point[0] for point in points]
# 删除特定名字的node和其关系
def deleteNode(node_name):
    db.cypher_query(
        '''
        Match (n) where n.title='{p}' DETACH delete n
        '''.format(p=node_name)
    )

def renewNode(title,Difficulty,Importance,Weights,Teached):
    db.cypher_query(
        '''
        match(n) where n.title='{p}' set n.Difficulty={d} set n.Importance={i} set n.Weights={j} set n.Teached={k}
        '''.format(p=title,d=Difficulty,i=Importance,j=Weights,k=Teached)
    )

def renewTestNode(title,testtype,Difficulty,Importance,Teached,testanswer,testcontent):
    db.cypher_query(
        '''
        match(n) where n.title='{p}' set n.Difficulty={d} set n.Importance={i} set n.Type={t} set n.Answer='{a}'
        '''.format(p=title,t=testtype, d=Difficulty, i=Importance, a=testanswer)
    )
    db.cypher_query(
        """
        match(n) where n.title='{p}' set n.Content='{testc}' set n.Teached={tea}
        """.format(p=title, testc=testcontent, tea=Teached)
    )
