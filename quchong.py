#coding:utf-8
'''第4步：对完整匹配的关键词pipei_word.py进行去重，保留字数最多的那一个'''

import sys,os,pycurl,StringIO,random,re,threading
from bs4 import BeautifulSoup as bs

inputfile,cigen,py = sys.argv[1:4]
os.system("python pipei.py %s %s %s" % (inputfile,cigen,py))
f = open('pipei_word.txt','r')
fd = open('pipei_word_1.txt','w')

def getUA():
    uaList = [
    'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+TencentTraveler)',
    'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.4506.2152;+.NET+CLR+3.5.30729)',
    'Mozilla/5.0+(Windows+NT+5.1)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.89+Safari/537.1',
    'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1)',
    'Mozilla/5.0+(Windows+NT+6.1;+rv:11.0)+Gecko/20100101+Firefox/11.0',
    'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+SV1)',
    'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)',
    'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+KB974489)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    ]
    ua = random.choice(uaList)
    return ua

headers = [
    "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding:gzip, deflate, sdch",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Connection:keep-alive",
    "Host:www.kanzhun.com",
    "RA-Sid:7739A016-20140918-030243-3adabf-48f828",
    "RA-Ver:2.8.9",
    "User-Agent:%s" % getUA()
    ]

def getHtml(url,headers):
    x = 0
    while x < 10:
        x += 1
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.MAXREDIRS,5)
            c.setopt(pycurl.REFERER, url)
            c.setopt(pycurl.FOLLOWLOCATION, True)
            c.setopt(pycurl.CONNECTTIMEOUT, 60)
            c.setopt(pycurl.TIMEOUT,120)
            c.setopt(pycurl.ENCODING,'gzip,deflate')
            #c.setopt(c.PROXY,ip)
            c.fp = StringIO.StringIO()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.HTTPHEADER,headers)
            c.setopt(c.WRITEFUNCTION, c.fp.write)
            c.perform()
            #code = c.getinfo(c.HTTP_CODE) 返回状态码
            content = c.fp.getvalue()

            # infoencode = chardet.detect(content).get('encoding','utf-8')
            # html = content.decode(infoencode,'ignore').encode(code)
            return content

        except:
            print "异常，重试>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            continue

url_list = []
for line in f:
    line = line.strip()
    url_list.append(line)


print ">>> 开始对同一个词被多次匹配的页面去重，保留正文字数最多的url......................................"

#<!-- 执行爬虫功能的类 -->
class getPic(threading.Thread):
    def __init__(self,url_list):
        threading.Thread.__init__(self)
        self.url_list = url_list
        self.timeout = 5

    #<!-- 此处为具体的实现功能，按需修改此处 -->
    def downloadimg(self):
        for line in self.url_list:
            url = line.split(',')[2]
            number = len(re.sub('<[^>]*?>','',str((bs(getHtml(url,headers))).find('div',{'id':'Article'}))))
            newline = '%s,%s' % (line,number)
            fd.write('%s\n' % newline)


    def run(self):
        self.downloadimg()

if __name__ == "__main__":
    getThreads = []
    checkThreads = []
    getPicThreads = []

#开启100线程,将url_list分成100份，每个线程运行1份
for i in range(5):
    t = getPic(url_list[((len(url_list)+4)/5) * i:((len(url_list)+4)/5) * (i+1)])
    getPicThreads.append(t)

for i in range(len(getPicThreads)):
    getPicThreads[i].start()

for i in range(len(getPicThreads)):
    getPicThreads[i].join()

print ">>> 完成"
print ">>> 合并处理文件"

os.system("cat pipei_word_1.txt|awk -F\",\" '{if($5~\"html\")print $1,$2,$3,$4,$5,$6}'|sort -k1n -k6nr|awk '!a[$1]++'|awk '{print $1\",\"$2\",\"$3\",\"$4\",\"$5}' > 1.txt")
os.system("cat pipei_word_1.txt|egrep -v 'html' > 2.txt")
os.system("cat 1.txt 2.txt > pipei_word.txt")
os.system("rm 1.txt 2.txt pipei_word_1.txt")
