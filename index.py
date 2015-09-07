#coding:utf-8
'''第六步：词库清洗系统主程序，执行所有子程序并格式化结果文件'''

import sys,os

inputfile,cigen,py = sys.argv[1:4]

os.system("python quchong.py %s %s %s" % (inputfile,cigen,py))
os.system("python fenci.py %s %s" % (cigen,py))


print "》》》数据统计："
print "新增列表词："
os.system("cat 新增列表词.txt|wc -l")

print "detail匹配词："
os.system("cat detail匹配词.txt|wc -l")

print "无结果词："
os.system("cat 无结果词.txt|wc -l")

os.system("rm nopipei_word.txt")
