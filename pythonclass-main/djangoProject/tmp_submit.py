# import sys
from random import sample
from os import listdir, rename
from os.path import splitext
import sys
import re
from pandas import Series, DataFrame
def readAnswer(path):
    file = open(path, encoding='utf-8')
    ans = []
    lineText = file.readline().split('\n')[0].split(',')
    while len(lineText) > 1:
        ans.append(lineText)
        lineText = file.readline().split('\n')[0].split(',')
    return ans

# # def tmp_function(answer):
flag = '1'
# 得到该学生的学号
username = sys.argv[1]
# 得到对应文件夹
l = sys.argv[2]
# 得到小测的名称
testname = sys.argv[3]
# 得到编程题的答案（编号），用来识别一个作业里的不同题目
test_num = sys.argv[4]
sys.path.append('./members/'+username+'/function_'+l)
# 读取function这个文件
with open("./members/"+username+'/function_'+l+"/function.py", encoding='utf-8') as f:
    tmp_l = len(f.readlines()[0].split(','))
# 导入文件
try:
    exec('from ' + 'function' + ' import fact')
except Exception as e:
    flag='0'
else:
    # 如果只有一个参数，就读取answer1
    # 参数个数决定运行fact的形式
    if testname == '第二次作业':
        if tmp_l == 1:
            answer1 = readAnswer('./answer/' + testname + '_answer1')
            for answer in answer1:
                if float(answer[1]) != fact(float(answer[0])):
                    flag = '2'
                    break
        if tmp_l == 2:
            answer2 = readAnswer('./answer/' + testname + '_answer2')
            for answer in answer2:
                answer = list(map(int, answer))
                # print(answer)
                answ = fact(answer[0], answer[1])
                if answ != answer[2]:
                    flag = '2'
                    break

    elif testname == '第三次作业':
        # if tmp_l == 1:
        answer1 = readAnswer('./answer/' + testname + '_answer1')
        for answer in answer1:
            answer = [int(x) for x in answer]
            line = answer[0]
            column = answer[1]
            input = []
            for i in range(line):
                tmp = []
                for j in range(column):
                    tmp.append(answer[i * column + j + 3])
                input.append(tmp)
            # 第三个元素是答案
            if float(answer[2]) != fact(input):
                flag = '2'
                break
    elif testname == '第四次作业':
        # count = 0
        if test_num == '1':
            listAnswer = [['Google', 'Microsoft', 'Apple'], ['Google', 'Microsoft', 'Apple', 'Facebook'],
                          ['Google', 'Oracle', 'Microsoft', 'Apple', 'Facebook'],
                          ['Apple', 'Facebook', 'Google', 'Microsoft', 'Oracle'], ['Google', 'Microsoft'],
                          ['Facebook', 'Google', 'Microsoft', 'Oracle'], ['Apple', 'Google', 'Oracle'],
                          ['Facebook', 'Microsoft'], ['Apple', 'Facebook', 'Google', 'Microsoft'],
                          ['Apple', 'Google', 'Microsoft']]
            # length = 5
            studentListAnswer, studentLen = fact()
            for i in range(len(studentListAnswer)):
                if listAnswer[i] != studentListAnswer[i]:
                    flag = '2'
                    break
                    # count = count + 1
                # else:
                #     print('right answer：', listAnswer[i], '  wrong answer;', studentListAnswer[i])

        elif test_num == '2':
            dictAnswer = [{'Beijing': '010', 'Guangzhou': '020'}, {'Beijing': '010', 'Guangzhou': '020', 'Shanghai': '021'}]
            # dictTag = False
            studentDictAnswer, studentTag = fact()
            for i in range(len(studentDictAnswer)):
                if dictAnswer[i] != studentDictAnswer[i]:
                    flag = '2'
                    break
                    # count = count + 1

        elif test_num == '3':
            setAnswer = [{1, 2, 3, 4}, {3, 4, 5, 6, 7}, {1, 2, 3, 4, 5}, {1, 2, 3, 5}, {3, 5}, {1, 2, 3, 4, 5, 6, 7}]
            studentSetAnswer = fact()
            for i in range(len(studentSetAnswer)):
                if setAnswer[i] != studentSetAnswer[i]:
                    flag = '2'
                    break

    elif testname == "第五次作业":
        minStack = fact()
        minStack.push(-1)
        minStack.push(0)
        minStack.push(-5)
        minStack.push(-2)
        minStack.push(-33)
        if minStack.getMin() != -33:  # 返回 - 33
            flag = '2'
        minStack.pop()
        if minStack.top() != -2:  # 返回  -2.
            flag = '2'
        if minStack.getMin() != -5:  # 返回 - 5.
            flag = '2'
        minStack.push(-33)
        if minStack.top() != -33:  # 返回  -33.
            flag = '2'
        if minStack.getMin() != -33:  # 返回 - 33
            flag = '2'
        minStack2 = fact()
        if minStack2.getClassTotal() != 2:  # 返回 2
            flag = '2'
        if fact.getStaticTotal() != 2:  # 返回 2
            flag = '2'

    elif testname == "第六次作业":
        def getAllWord(textString):
            textWordList = re.findall(r'[a-zA-Z]+', textString)
            newWordList = []
            for word in textWordList:
                if len(word) > 2:
                    word = word.lower()
                    newWordList.append(word)
            return newWordList

        def getWord():
            # 读取所有的文件
            textWordList = []
            for i in range(1, 26):
                wordList = getAllWord(open('./email/spam/%d.txt' % i, encoding='ISO-8859-15').read())
                textWordList.append(wordList)
                wordList = getAllWord(open('./email/ham/%d.txt' % i, encoding='ISO-8859-15').read())
                textWordList.append(wordList)
            word = {}
            for i in range(0, len(textWordList)):
                for j in range(0, len(textWordList[i])):
                    if textWordList[i][j] not in word.keys():
                        word[textWordList[i][j]] = 1
                    else:
                        word[textWordList[i][j]] = word[textWordList[i][j]] + 1
            return word
        
        count = 0
        wordKDict = getWord()
        studentWord = fact('./email/')
        for key in wordKDict.keys():
            if key in studentWord.keys():
                if studentWord[key] == wordKDict[key]:
                    count = count + 1
        # 满分是100左右，小于60及格线就算错
        if count <= 60:
            flag = '2'

    elif testname == "第七次作业":
        count = 0
        from answer.a07 import getAnswers

        answer, _ = getAnswers()
        studentAnswer, _ = fact()
        # studentAnswer = fact()
        for i in range(len(answer)):
            if (answer[i] == studentAnswer[i]).all():
                count = count + 1

        len_ans = len(answer)
        score = 100 * count / len_ans
        if score<60:
            flag = '2'

    elif testname == "第八次作业":
        test_num = sys.argv[4]
        count = 0
        from answer.a08 import getSeries1,getDataFrame1
        studentAnswer = fact()

        if test_num == '1':
            answer = getSeries1()
            for i in range(len(answer)):
                if i == 3:
                    if answer[i] == studentAnswer[i]:
                        count = count + 1
                else:
                    if answer[i].equals(studentAnswer[i]):
                        count = count + 1

        elif test_num == '2':
            answer = getDataFrame1()
            for i in range(len(answer)):
                if answer[i].equals(studentAnswer[i]):
                    count = count + 1

        len_ans = len(answer)
        score = 100 * count / len_ans
        if score < 60:
            flag = '2'


    elif testname == "第九次作业":

        count = 0

        from answer.a09 import getAnswers

        answer = getAnswers()

        studentAnswer = fact()

        for i in range(len(answer)):

            if answer[i].equals(studentAnswer[i]):
                count = count + 1

        score = 100 * count / len(answer)

        if score < 95:
            flag = '2'


    elif testname == "第十次作业":

        pass
print (flag)