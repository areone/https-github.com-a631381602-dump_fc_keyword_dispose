#coding:utf-8
'''第三部：将凤巢关键词与上线关键词进行对比，完整匹配的存入pipei_word.txt待去重，未匹配存入nopipei_word.txt待分词判断相关性来挑选合适的着陆页页面'''

import csv,os,sys

inputfile,cigen,py = sys.argv[1:4]

os.system("python fcword.py %s %s" % (inputfile,cigen))
os.system("python sqldata.py %s %s" % (cigen,py))
os.system("cat sqldata*.csv > hebing.csv")
os.system("rm sqldata*.csv")

csv.field_size_limit(sys.maxsize)
f = open('fcword.txt','r')
p = open('pipei_word.txt','w')      #创建完整匹配关键词存放文件
np = open('nopipei_word.txt','w')   #创建未完整匹配关键词存放文件

print ">>> 开始将凤巢关键词与上线关键词进行对比......................................"

w = 0
n = 0
for term in f:  #读取凤巢关键词
    term = term.strip()
    word = term.split(',')[0]
    searches = term.split(',')[1]

    panding = 'no'  #匹配判定，若完整匹配一次，则panding = word
    reader = csv.reader(file('hebing.csv','rb'))
    for line in reader:
        word_name = line[0]
        word_url = line[1]

        if word == word_name:   # 匹配的关键词存入'pipei_word.txt'
            panding = word
            p.write("%s,%s,%s\n" % (word,searches,word_url))
            n += 1
        else:
            continue

    if panding == 'no':     #未匹配关键词存入'nopipei-word.txt'
        np.write("%s,%s\n" % (word,searches))
        w += 1

os.system("rm hebing.csv")

print ">>> 匹配结束......................................"
print ">>> 完整匹配关键词数：%s" % str(n)
print ">>> 未匹配关键词数：%s" % str(w)
