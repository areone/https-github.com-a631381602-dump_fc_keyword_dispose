#coding:utf-8
'''
第五步：
1、剩余未完整匹配上的凤巢搜索词跑下站内搜索，提取并计算‘搜索结果数’，‘整词召回数’，‘主词召回数’，根据以上指标判定该词是否生成专题页还是匹配相似详情页title
    ps：新增专题数量需要限制
'''

import sys,os,pycurl,StringIO,random,re,threading,urllib
from bs4 import BeautifulSoup as bs

cigen,py = sys.argv[1:3]

f = open('nopipei_word.txt','r')
zt = open('新增列表词.txt','w')
wjg = open('无结果词.txt','w')
xgt = open('detail匹配词.txt','w')

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

def search(req,html):
     text = re.search(req,html)
     if text:
         data = text.group(1)
     else:
         data = 'no'
     return data

print ">>> 开始导入站内搜索url......................................"
url_list = []
for line in f:
    line = line.strip()
    url = 'http://www.domain.com/phpcms/api/search-2.php?query=%s' % urllib.quote(line.split(',')[0])
    newline = '%s,%s' % (line,url)
    url_list.append(newline)


print ">>> 完成"
print ">>> 开始判定该词是否生成专题页还是匹配相似详情页title......................................"

detail_word_list = []
#<!-- 执行爬虫功能的类 -->
class getPic(threading.Thread):
    def __init__(self,url_list):
        threading.Thread.__init__(self)
        self.url_list = url_list
        self.timeout = 5

    #<!-- 此处为具体的实现功能，按需修改此处 -->
    def downloadimg(self):
        for line in self.url_list:
            word = line.split(',')[0]
            searches = line.split(',')[1]
            url = line.split(',')[2]
            html = getHtml(url,headers)
            #jieguo = re.sub('\(.*?\)|&[^;]*?;','',search('<b>分词结果:</b>(.*?)<hr>',html)).replace('-','')

            panding = re.sub(cigen,'',word)

            n = 0   #主词召回
            m = 0   #整词召回
            title_list = re.findall('<a[^>]*?>(.*?)</a>',html)  #获取搜索结果的title生成列表

            for title in title_list:    # 比如‘网络营销策划书’，计算搜索结果中包含‘网络营销’和‘网络营销策划书’的详情页个数
                if word in title:
                    m += 1
                if panding in title:
                    n += 1

            if  m == 0 or n == 0: # 计算包含完成word，即‘网络营销策划书’的召回率
                ratio = '0'
            else:
                ratio = str(format(float(int(m))/float(int(n)),'.0%')).replace('%','')

            number = search('b>结果数量：</b>(\d+)&',html)  #获取word搜索结果数量

            if int(number) >= 10 and n >5 :  # 生成专题的判定条件
                zt.write("%s,%s\n" % (word,searches))
                #print word,searches,number
            else:
                if number == '0':                               #无搜索结果的词存入‘无结果词’文件中
                    #print word,searches,number
                    wjg.write("%s,%s\n" % (word,searches))
                else:
                    if int(searches) > 70 and int(number) >=10:      #搜索结果>10且searches>70补加到生成专题词中
                        zt.write("%s,%s\n" % (word,searches))
                        #print word,searches,number
                    else:
                        detail = search(r"href='(http://www.domain.com/%s/[^']*?)'" % py,html)    #需更改title的详情页
                        if detail not in detail_word_list:                                          
                            if detail != 'no':
                                xgt.write("%s,%s,%s\n" % (word,searches,detail))
                                #print word,searches,detail,number
                                detail_word_list.append(detail)
                            else:
                                wjg.write("%s,%s\n" % (word,searches))

    def run(self):
        self.downloadimg()

if __name__ == "__main__":
    getThreads = []
    checkThreads = []
    getPicThreads = []

#开启100线程,将url_list分成100份，每个线程运行1份
for i in range(3):
    t = getPic(url_list[((len(url_list)+2)/3) * i:((len(url_list)+2)/3) * (i+1)])
    getPicThreads.append(t)

for i in range(len(getPicThreads)):
    getPicThreads[i].start()

for i in range(len(getPicThreads)):
    getPicThreads[i].join()

print '>>> 完成'
