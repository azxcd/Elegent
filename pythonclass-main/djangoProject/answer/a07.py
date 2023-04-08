#coding=utf-8
import numpy as np

def getAnswers():
    answer=[]
    #  创建一维的narray对象arr1，内有元素1，2，3，4，5，6，7，8，9要求使用arange()函数
    arr1 = np.arange(1,10)
    # 将结果添加到answer，用于检查
    answer.append(arr1.copy())

    #  将arr1转换成3*3的矩阵arr2
    arr2 = arr1.reshape(3, 3)
    # 将结果添加到answer，用于检查
    answer.append(arr2.copy())

    #  使用linsapce()函数，生成首位是0，末位是10，含5个数的等差数列arr3,元素类型为float
    arr3 = np.linspace(0, 10, 5,dtype=float)
    # 将结果添加到answer，用于检查
    answer.append(arr3.copy())

    #  创建3*4的全1矩阵arrOnes，元素类型为int
    arrOnes = np.ones((3, 4),dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(arrOnes.copy())

    #  创建3*4的全0矩阵arrZeros，元素类型为int
    arrZeros = np.zeros((3, 4),dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(arrZeros.copy())

    #  创建3阶单位矩阵arrUnit，元素类型为int
    arrUnit = np.eye(3,dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(arrUnit.copy())

    #  创建一个3*3的矩阵matrix1，内有元素[[1,3,3],[6,5,6],[9,9,9]],元素类型为int
    matrix1 = np.array([[1,3,3],[6,5,6],[9,9,9]],dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(matrix1.copy())

    #  获取矩阵matrix1的逆为matrix2
    matrix2 = np.linalg.inv(matrix1)
    # 将结果添加到answer，用于检查
    answer.append(matrix2.copy())

    #  打印矩阵matrix1中的最大值
    maxOfMatrix1=matrix1.max()

    #  打印矩阵matrix1每一列的最大值
    ColumnMax=matrix1.max(axis=0)
    # 将结果添加到answer，用于检查
    answer.append(ColumnMax.copy())

    #  打印矩阵matrix1每一行的平均值
    LineMean = matrix1.mean(axis=1)
    # 将结果添加到answer，用于检查
    answer.append(LineMean.copy())

    #  打印矩阵matrix1每一列的方差
    variance = matrix1.var(axis=0)
    # 将结果添加到answer，用于检查
    answer.append(variance.copy())

    #  截取矩阵matrix1的第1，2行，存到matrix3
    matrix3 = matrix1[0:2]
    # 将结果添加到answer，用于检查
    answer.append(matrix3.copy())

    #  截取矩阵matrix1的第1，2行，第2，3列,存到matrix4
    matrix4 = matrix1[0:2, 1:3]
    # 将结果添加到answer，用于检查
    answer.append(matrix4.copy())

    #  截取矩阵matrix1中大于3的元素
    maxList = matrix1[matrix1 > 3]
    # 将结果添加到answer，用于检查
    answer.append(maxList.copy())

    return answer,maxOfMatrix1


def getAnswers1():
    answer=[]
    #  创建一维的narray对象arr1，内有元素1，2，3，4，5，6，7，8，9要求使用arange()函数
    arr1 = np.arange(1,10)
    # 将结果添加到answer，用于检查
    answer.append(arr1.copy())

    #  将arr1转换成3*3的矩阵arr2
    arr2 = arr1.reshape(3, 3)
    # 将结果添加到answer，用于检查
    answer.append(arr2.copy())

    #  使用linsapce()函数，生成首位是0，末位是10，含5个数的等差数列arr3,元素类型为float
    arr3 = np.linspace(0, 10, 5,dtype=float)
    # 将结果添加到answer，用于检查
    answer.append(arr3.copy())

    #  创建3*4的全1矩阵arrOnes，元素类型为int
    arrOnes = np.ones((3, 4),dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(arrOnes.copy())

    #  创建3*4的全0矩阵arrZeros，元素类型为int
    arrZeros = np.zeros((3, 4),dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(arrZeros.copy())

    #  创建3阶单位矩阵arrUnit，元素类型为int
    arrUnit = np.eye(3,dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(arrUnit.copy())

    #  创建一个3*3的矩阵matrix1，内有元素[[1,2,3],[4,5,6],[7,8,9]],元素类型为int
    matrix1 = np.matrix([[1,3,3],[6,5,6],[9,9,9]],dtype=int)
    # 将结果添加到answer，用于检查
    answer.append(matrix1.copy())

    #  获取矩阵matrix1的逆为matrix2
    matrix2 = np.linalg.inv(matrix1)
    # 将结果添加到answer，用于检查
    answer.append(matrix2.copy())

    #  打印矩阵matrix1中的最大值
    maxOfMatrix1=matrix1    ()

    #  打印矩阵matrix1每一列的最大值
    ColumnMax=matrix1.max(axis=0)
    # 将结果添加到answer，用于检查
    answer.append(ColumnMax.copy())

    #  打印矩阵matrix1每一行的平均值
    LineMean = np.mean(matrix1,axis=1)
    # 将结果添加到answer，用于检查
    answer.append(LineMean.copy())

    #  打印矩阵matrix1每一列的方差
    variance = matrix1.var(axis=0)
    # 将结果添加到answer，用于检查
    answer.append(variance.copy())

    #  截取矩阵matrix1的第1，2行，存到matrix3
    matrix3 = matrix1[0:2]
    # 将结果添加到answer，用于检查
    answer.append(matrix3.copy())

    #  截取矩阵matrix1的第1，2行，第2，3列,存到matrix4
    matrix4 = matrix1[0:2, 1:3]
    # 将结果添加到answer，用于检查
    answer.append(matrix4.copy())

    #  截取矩阵matrix1中大于3的元素
    maxList = matrix1[matrix1 > 3]
    # 将结果添加到answer，用于检查
    answer.append(maxList.copy())

    return answer,maxOfMatrix1

