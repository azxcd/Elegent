#coding=utf-8

# 从pandas库导入Series,DataFrame
from pandas import Series, DataFrame

def getSeries1():
    # 定义answer，用于检查结果是否正确,用于批改作业
    answer =[]
    # 创建列表lst
    lst = [4, 7, -5, 3]

    # 使用列表list生成Series对象obj
    obj = Series(lst)  # obj =
    # 将结果添加到answer，用于检查
    answer.append(obj)


    # 创建数组index
    index1 = ['d', 'b', 'a', 'c']

    # 创建数据为lst，索引为index1的Series对象obj2
    obj2 = Series(lst, index1)  # obj2=
    # 将结果添加到answer，用于检查
    answer.append(obj2.copy())

    # 将obj2中索引值为d对应的值赋值为6
    obj2['d'] = 6  #
    # 将结果添加到answer，用于检查
    answer.append(obj2.copy())

    # 打印obj2中索引值为d对应的值
    ans1 = obj2['d']
    # 将结果添加到answer，用于检查
    answer.append(ans1)
    #print(ans1.equals(ans1.copy()))

    # 从obj2找出大于0的元素并打印
    ans2 = obj2[obj2 > 0]
    # 将结果添加到answer，用于检查
    answer.append(ans2)


    #  创建字典sdata
    sdata = {'Ohio': 45000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}

    #  利用sdata生成Series对象obj3
    obj3 = Series(sdata)  # obj3=
    # 将结果添加到answer，用于检查
    answer.append(obj3)



    # 创建列表states
    states = ['California', 'Ohio', 'Oregon', 'Texas']

    # 创建数据为sdata，索引为states的Series对象obj4
    obj4 = Series(sdata, index=states)  # obj4=
    # 将结果添加到answer，用于检查
    answer.append(obj4)


    # 将obj3和obj4进行相加，相同索引部分相加，存储到obj5
    obj5 = obj3 + obj4
    # 将结果添加到answer，用于检查
    answer.append(obj5)


    # 指定obj4的名字为population
    obj4.name = 'population'  #
    # 将结果添加到answer，用于检查
    answer.append(obj4)

    # 指定obj4的索引的名字为state
    obj4.index.name = 'state'  #
    # 将结果添加到answer，用于检查
    answer.append(obj4)

    return answer


def getDataFrame1():

    answer = []
    # 创建字典data
    data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}

    # 创建列表col，index1
    col = ['year', 'state', 'pop', 'debt']
    index1 = ['one', 'two', 'three', 'four', 'five']

    # 利用data创建DataFrame对象frame1,并指定该对象列为col，索引为index1
    frame1 = DataFrame(data, columns=col, index=index1)  # frame1 =
    # 将结果添加到answer，用于检查
    answer.append(frame1.copy())

    # 排序
    # 根据索引，对frame1进行降序排序，并指定轴为1
    frame2 = frame1.sort_index(axis=1, ascending=False)
    # 将结果添加到answer，用于检查
    answer.append(frame2.copy())

    # 根据值，对frame1的year列进行排序(升序）并打印
    frame3 = frame1.sort_values(by='year')
    # 将结果添加到answer，用于检查
    answer.append(frame3.copy())

    # 处理缺失数据
    # 对于frame1，只要有某行有NaN就全部删除
    frame4 = frame1.dropna()
    # 将结果添加到answer，用于检查
    answer.append(frame4.copy())

    # 对于frame1，某行全部为NaN才删除
    frame5 = frame1.dropna(how='all')
    # 将结果添加到answer，用于检查
    answer.append(frame5.copy())

    # 填充缺失数据
    # 对于frame1，将元素为NaN替换成0
    frame6 = frame1.fillna(0)
    # 将结果添加到answer，用于检查
    answer.append(frame6.copy())

    return answer

