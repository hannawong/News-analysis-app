
# coding = unicode


import re
import time
import requests
import pandas as pd
import jieba
import sys
sys.path.append("/home/ubuntu/backend/xxswl-backend/")
print(sys.path)
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()

from news.models import Articles
from news.models import WeiboHot


def crawler_weibo_hot(): 
    WeiboHot.objects.all().delete()
    url = 'https://s.weibo.com/top/summary/summary?cate=realtimehot'
    strhtml = requests.get(url).text
    pattern0 = r"<a href=(?P<url>.*Refer=.*)target=.*>(?P<title>.*)</a>\n.*<span>(?P<hot>\d*)</span>"
    it = re.finditer(pattern0, strhtml)
    id = 0
    for match in it:
        hot = WeiboHot()
        hot.id = id
        id += 1
        hot.title = match.group("title")
        hot.hot = match.group("hot")
        hot.title+="@"+str("https://s.weibo.com"+match.group("url")[1:-2])
        hot.save()
        print("写入微博热搜")
crawler_weibo_hot()


delta_time = 60 # *60*3 
IDF_contains_doc={}
def news_crawler():  
    global IDF_contains_doc
    url_list = []
    sina_rollnews = Articles.objects.filter()
    doc_num=len(sina_rollnews)  
    print(sina_rollnews, "=============================")

    pre_url = Articles.objects.values_list("url")  
    pre_url_list = []
    for i in range(max(0, len(pre_url)-100), len(pre_url)):
        pre_url_list.append(pre_url[i][0])
    print(pre_url_list)
    init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/55.0.2883.87 Safari/537.36'}
    page = requests.get(url=init_url.format(1)).json()
    for j in range(50):
        urls = page['result']['data'][j]['wapurl']
        print(j, "   ", urls)
        if urls in pre_url_list:
            print("already in database, skipping....")
        else:
            try:
                text = requests.get(urls).text
                url_list.append(urls)
            except:
                print("no")
                continue
            # print(text)
            pattern0 = "<title>(?P<title>.+?)_.*?</title>"
            pattern1 = "published_time\" content=\"(?P<time>.*?)\""
            pattern2 = "<meta name=\"author\" content=\"(?P<author>.*?)\""
            pattern3 = "<meta name=\"publishid\" content=\"(?P<id>.*?)\""
            pattern4 = "<p.*?>(?P<text>.*?)</p>"
            pattern5 = "<.*?>"
            title = ""
            time = ""
            author = ""
            publish_id = ""
            it = re.finditer(pattern0, text)
            for match in it:
                title = match.group("title")
            it1 = re.finditer(pattern1, text)
            for match in it1:
                time = match.group("time")
            it2 = re.finditer(pattern2, text)
            for match in it2:
                author = match.group("author")
            it3 = re.finditer(pattern3, text)
            for match in it3:
                publish_id = match.group("id")
            it4 = re.finditer(pattern4, text)
            body = ""
            for match in it4:
                body += match.group("text")
            body = re.sub(pattern5, "", body)  
            news = Articles()
            news.url = urls
            news.title = title
            news.time = time
            news.author = author
            news.publish_id = publish_id
            news.body=body
            doc_num += 1
            news.save()
            print("done")

while 1: 
    news_crawler()
    time.sleep(delta_time)
