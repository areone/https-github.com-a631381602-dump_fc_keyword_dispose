# coding:utf-8
'''第一步：凤巢关键词，排除包含空格，并保留searches>5且包含词根的关键词，输出到制定csv文件
凤巢关键词扩展处理视情况处理下，去除与词根完全没关联的词，后保存为“word-search”两列数据即可

inputfile == 凤巢关键词
cigen == 凤巢关键词需要包含的词，一般为上线频道名称


BUG归总：
1、匹配出要上线的列表词与已上线频道的关键词重复
   解决办法：将第三部（pipei.py）中的匹配范围由匹配当前频道改为匹配所有频道上线关键词，修改第二部sqldata.py中的sql即可

2、匹配出需要改title的关键词匹配上多个title
   解决办法：在第五步（fenci.py）中处理，新建一个list，每次搜索关键词，当属于本频道最靠前的结果出现在这个list中，则选取先一个结果，依此循环

'''

import csv,sys,MySQLdb,sys,pypinyin,csv,os

inputfile,cigen = sys.argv[1:3]

csv.field_size_limit(sys.maxsize)
reader = csv.reader(file(inputfile,'rb'))
csvfile = open('fcword.txt','wb')

word_list = []

print ">>> 开始过滤凤巢关键词......................................"

for line in reader: #读取凤巢关键词，分离关键词和对应的搜索量
    try:
        word = line[0]
        searches = line[1]

        if ' ' not in word and '的' not in word and cigen in word and int(searches)>5:   #排除凤巢关键词中带空格，包含上线频道词根及搜索量大于词
            term = '%s-%s' % (word,searches)
            word_list.append(term)
    except:
        continue

print ">>> 关键词过滤完成......................................"
print ">>> 过滤结果写入fcword.txt......................................"

for term in list(set(word_list)):   #过滤后关键词写入fcword.txt
    word = term.split('-')[0]
    searches = term.split('-')[1]

    data = []
    data.append(word)
    data.append(searches)

    writer = csv.writer(csvfile,dialect='excel')
    writer.writerow(data)

print ">>> fcword.txt写入完成......................................"




