#coding=utf-8

# 导入相关的包
import pandas as pd
import numpy as np
from numpy import nan as NA

def getAnswers():
    # 定义answer，用于检查结果是否正确,用于批改作业
    answer = []

    df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': range(7)})
    df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'data2': range(3)})

    # 指定key这一列取交集
    dataframe1 = pd.merge(df1, df2, on='key')

    # 将结果添加到answer，用于检查
    answer.append(dataframe1)

    # 取df1和df2的交集
    dataframe2 = pd.merge(df1, df2)

    # 将结果添加到answer，用于检查
    answer.append(dataframe2)

    # 取左连接，df1
    dataframe3 = pd.merge(df1, df2, on='key', how='left')

    # 将结果添加到answer，用于检查
    answer.append(dataframe3)

    df3 = pd.DataFrame({"lkey": ["b", "b", "a", "c", "a", "a", "b"], "data1": range(7)})
    df4 = pd.DataFrame({"rkey": ["a", "b", "d"], "data2": range(3)})

    # 取df3，df4的交集
    dataframe4 = pd.merge(df3, df4, left_on='lkey', right_on='rkey')

    # 将结果添加到answer，用于检查
    answer.append(dataframe4)

    s1 = pd.Series([0, 1], index=["a", "b"])
    s2 = pd.Series([2, 3, 4], index=["c", "d", "e"])
    s3 = pd.Series([5, 6], index=["f", "g"])

    # 将多个Series拼接成一个DataFrame,即一个Series就是DataFrame的一列数据
    dataframe6 = pd.concat([s1, s2, s3], axis=1)
    # 将结果添加到answer，用于检查
    answer.append(dataframe6)


    df5 = pd.DataFrame({"a": [1, NA, 5, NA], "b": [NA, 2, NA, 6], "c": range(2, 18, 4)})
    df6 = pd.DataFrame({"a": [5, 4, NA, 3, 7], "b": [NA, 3, 4, 6, 8]})

    # 用df6的数据为df5中的数据打补丁
    dataframe7 = df5.combine_first(df6)

    # 将结果添加到answer，用于检查
    answer.append(dataframe7)

    data = pd.DataFrame(np.arange(6).reshape(2, 3), index=pd.Index(["上海", "北京"], name="省份"),
                        columns=pd.Index([2011, 2012, 2013], name="年份"))
    # 将data的列索引转换到行索引
    result1 = data.stack()

    # 将结果添加到answer，用于检查
    answer.append(result1)

    # 将result1的行索引转化为列索引
    result2 = result1.unstack()

    # 将结果添加到answer，用于检查
    answer.append(result2)

    # 将result1的行索引转化为列索引，指定要转化为层次化索引的名称为"省份"
    result3 = result1.unstack("省份")

    # 将结果添加到answer，用于检查
    answer.append(result3)

    data1 = pd.DataFrame({"k1": ["one"] * 3 + ["two"] * 4, "k2": [1, 1, 2, 3, 3, 4, 4]})
    # 使用DataFrame的内置函数去除重复数据，默认保留第一次出现的值
    result4 = data1.drop_duplicates()

    # 将结果添加到answer，用于检查
    answer.append(result4)

    return answer






