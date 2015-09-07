#coding:utf-8
'''第二步：获取包含制定词根（同凤巢扩展关键词使用词根一致）的上线词及详情'''

import MySQLdb,sys,pypinyin,csv,os
from pypinyin import pinyin, lazy_pinyin

cigen,py = sys.argv[1:3]
csvfile1 = open('sqldata1.csv','wb')
csvfile2 = open('sqldata2.csv','wb')
csvfile3 = open('sqldata3.csv','wb')

#py = ''.join(lazy_pinyin(unicode("%s" % cigen,"utf-8")))

# 打开数据库连接
db = MySQLdb.connect("{ip}","{user_name}","{password}","{data_name}" )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# sql_z = 'select title,url from v9_zhuanti where url like "%%%s%%";' % py
# sql_l = 'select catname,url from v9_category where url like"%%%s%%";' % py
# sql_d = 'select title,url from v9_news where url like"%%%s%%";' % py

##bug修复，匹配范围改为所有频道
sql_z = 'select title,url from v9_zhuanti;' 
sql_l = 'select catname,url from v9_category;'
sql_d = 'select title,url from v9_news'

print ">>> 开始从mysql获取%s频带关键词数据......................................" % cigen

print ">>> 获取专题关键词中......................................"
# 提取包含词根的专题关键词
cursor.execute(sql_z)
results = cursor.fetchall()
nz = 0
for row in results:
    zhuanti_name = row[0]
    zhuanti_url = row[1]

    nz += 1
    data = []
    data.append(zhuanti_name)
    data.append('http://www.domain.com/%s' % zhuanti_url)
    writer = csv.writer(csvfile1,dialect='excel')
    writer.writerow(data)


print ">>> 获取栏目关键词中......................................"
# 提取包含词根的栏目关键词
cursor.execute(sql_l)
results = cursor.fetchall()
nl = 0
for row in results:
    lanmu_name = row[0]
    lanmu_url = row[1]

    nl += 1
    data = []
    data.append(lanmu_name)
    data.append('http://www.domain.com/%s' % lanmu_url)
    writer = csv.writer(csvfile2,dialect='excel')
    writer.writerow(data)


print ">>> 获取详情关键词中......................................"
# 提取包含词根的详情页
cursor.execute(sql_d)
results = cursor.fetchall()
nd = 0
for row in results:
    detail_name = row[0]
    detail_url = row[1]

    nd += 1
    data = []
    data.append(detail_name)
    data.append('http://www.domain.com/%s' % detail_url)
    writer = csv.writer(csvfile3,dialect='excel')
    writer.writerow(data)

print ">>> 获取栏目：%s" % str(nl)
print ">>> 获取专题：%s" % str(nz)
print ">>> 获取详情：%s" % str(nd)

#关闭数据库连接
db.close()


print ">>> 关闭mysql连接......................................"
