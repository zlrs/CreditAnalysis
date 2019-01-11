'''
@usage
1. 从教务系统复制课程数据，不要复制表头
http://eams.uestc.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR
2. 粘贴到excel中，方式选纯文本粘贴
3. 复制excel中的数据到脚本同目录的data.txt文件中并保存
4. 运行脚本
@feedback
zhuys123@gmail.com
'''
classes = []
# read classes data
with open("./data.txt", encoding='utf-8') as f:
    for s in f.readlines():
        items = s.split("\t")
        classCode = items[1]
        className = items[3]
        classType_Chinese = items[4]
        credit = items[5]
        score = items[6]
        classes.append({"classCode": classCode,
            "className": className,
            "classType_Chinese": classType_Chinese,
            "credit": credit,
            "score": score
            })

# sort classes by classCode
classes.sort(key=lambda x:x['classCode'])

# print out to file and terminal
preType = 'A'
sum = 0
totalCredit = 0
Typecount = 1

fout = open("out.txt", "w", encoding='utf-8')
for cls in classes:
    classType = cls['classCode'][0]
    if classType != preType:
        line = '*{}* {}类课程总学分：{}'.format(Typecount, preType, sum)
        print(line)
        fout.write(line)
        fout.write('\n')
        preType = classType
        totalCredit += sum
        sum = 0
        Typecount += 1
    sum += float(cls['credit'])
    line = '\t'.join((cls["classCode"], cls['credit'], cls['score'], cls['classType_Chinese'], cls['className']))
    print(line)
    fout.write(line)
    fout.write('\n')

print('*{}* {}类课程总学分：{}'.format(Typecount, preType, sum))
fout.write('*{}* {}类课程总学分：{}\n'.format(Typecount, preType, sum))
print('总学分：{}'.format(totalCredit))
fout.write('总学分：{}\n'.format(totalCredit))
fout.close()
