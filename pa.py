# -*- coding: cp936 -*-
#python 2.7.13
import requests
import re
from urllib import quote

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# ���ð�ȫ���󾯸�
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://www.baidu.com/s?wd=%s&pn=%d"
wd = raw_input("�����ѯ�ؼ��֣�")
wd = quote(wd)
pn = raw_input("������Ҫ�ɼ���������")
pn = int(pn)

print

count = 1
pn10 = 0


def page1(url , pn , count):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    response = requests.get(url , verify=False , headers = headers)
    response2 = response.content.decode('UTF-8')
    pattern = '''<h3 class="t"><a [\s\S]*?href = "(.*?)"[\s\S]*?>([\s\S]*?)</a></h3>'''

    for x in re.findall(pattern , response2):
        if count<=pn:
            result = x[1].replace('<em>','').replace('</em>','')
            print count,result
            url2 = x[0]
            response2 = requests.head(url2 , verify=False)
            print response2.headers['Location']
            print
            count += 1
        else:
            return 0

    return count

while count <= pn:
    url2 = url%(wd,pn10)
    count = page1(url2 , pn , count)
    if count != 0:
        pn10 += 10
    else:
        break
