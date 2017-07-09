# -*- coding: cp936 -*-
#python 2.7.13
import requests
import re
from urllib import quote

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def page1(url , pn , count):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    response = requests.get(url , verify=False , headers = headers)
    response2 = response.content.decode('UTF-8')
    pattern = '''<h3 class="t"><a [\s\S]*?href = "(.*?)"[\s\S]*?>([\s\S]*?)</a></h3>'''

    for x in re.findall(pattern , response2):
        if count<=pn:#已爬数目小于需要采集条数
            result = x[1].replace('<em>','').replace('</em>','').replace(' ','')
            url2 = x[0]
            response3 = requests.head(url2 , verify=False)
            url3 = response3.headers['Location']
            #得到真实网址url3
            
            try:
                response4 = requests.get(url3,verify=False,headers=headers)
                if response4.status_code==200:
                    print count,
                    if url3 != response4.url:#判断真实网址后面是否有做301等跳转
                        print result
                        print url3
                    try:
                        title = re.findall("<title>([\s\S]*?)</title>",response4.content)[0]
                        try:
                            title = title.decode('UTF-8')
                        except:
                            pass
                        print title.replace('\n','').replace('\t','').replace(' ','')
                    except:
                        print "正则匹配title失败，百度搜索结果为：",result
                    print response4.url
                else:
                    print count,resul
                    print url3
                    print response4.status_code,"已死"
            except:
                print result
                print url3
                print "请求真实网址失败"
            print
            count += 1
        else:
            return 0
    return count


url = "https://www.baidu.com/s?wd=%s&pn=%d"
wd = raw_input("输入查询关键字：")
wd = quote(wd)
pn = raw_input("输入需要采集的条数：")
pn = int(pn)

count = 1
#目前已爬条数
pn10 = 0
#当前页数，每10条为一页

print

while count <= pn:
    url2 = url%(wd,pn10)
    count = page1(url2 , pn , count)
    if count != 0:
        pn10 += 10
    else:
        break
