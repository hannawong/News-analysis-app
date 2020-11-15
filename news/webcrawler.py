# coding = unicode

import time
import requests
import sys
sys.path.append("/home/ubuntu/xxswl-backend/")
sys.path.append("/home/ubuntu/wzh/xxswl-backend/")
sys.path.append("D:\\Program Files\\PycharmProjects\\xxswl-backend")
from news.re_funcs import re_finditer, re_sub
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()
from news.models import Articles
from news.models import WeiboHot
from news.models import WeiboSocialEvents


def crawler_weibo_hot():
    WeiboHot.objects.all().delete()
    url = 'https://s.weibo.com/top/summary/summary?cate=realtimehot'
    strhtml = requests.get(url).text
    pattern0 = r"<a href=(?P<url>.*Refer=.*)target=.*>(?P<title>.*)</a>\n.*<span>(?P<hot>\d*)</span>"
    it = re_finditer(pattern0, strhtml)
    id = 0
    for match in it:
        hot = WeiboHot()
        hot.id = id
        id += 1
        hot.title = match.group("title")
        hot.hot = match.group("hot")
        hot.title += "@" + str("https://s.weibo.com" + match.group("url")[1:-2])
        hot.save()
        print("写入微博热搜")


def crawl_weibo_socialevents():
    WeiboSocialEvents.objects.all().delete()
    url = 'https://s.weibo.com/top/summary/summary?cate=socialevent'
    strhtml = requests.get(url).text
    pattern0 = r"<a href=\"(?P<url>.*?)\".*?>(?P<title>#.*#)</a>"
    it = re_finditer(pattern0, strhtml)
    id = 0
    for match in it:
        hot = WeiboSocialEvents()
        hot.id = id
        id += 1
        hot.title = match.group("title")
        hot.title += "@" + str("https://s.weibo.com" + match.group("url"))
        hot.save()
        print("写入微博要闻")


crawler_weibo_hot()
crawl_weibo_socialevents()

delta_time = 60  # *60*3
IDF_contains_doc = {}


def news_crawler():
    global IDF_contains_doc
    url_list = []
    sina_rollnews = Articles.objects.filter()
    doc_num = len(sina_rollnews)
    print(sina_rollnews, "=============================")
    init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/55.0.2883.87 Safari/537.36'}
    for k in range(0,50):
        print(k,"====================")
        pre_url = Articles.objects.values_list("url")
        pre_url_list = []
        for i in range(0, len(pre_url)):
            pre_url_list.append(pre_url[i][0])
        page = requests.get(url=init_url.format(k)).json()
        for j in range(len(page['result']['data'])):
            urls = page['result']['data'][j]['wapurl']
            print(j, "   ", urls)
            if urls in pre_url_list:
                print("already in database, skipping....")
            else:
                try:
                    text = requests.get(urls).text
                    url_list.append(urls)
                except Exception:
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
                it = re_finditer(pattern0, text)
                for match in it:
                    title = match.group("title")
                it1 = re_finditer(pattern1, text)
                for match in it1:
                    time = match.group("time")
                it2 = re_finditer(pattern2, text)
                for match in it2:
                    author = match.group("author")
                it3 = re_finditer(pattern3, text)
                for match in it3:
                    publish_id = match.group("id")
                it4 = re_finditer(pattern4, text)
                body = ""
                for match in it4:
                    body += match.group("text")
                body = re_sub(pattern5, "", body)
                news = Articles()
                news.url = urls
                news.title = title
                news.time = time
                news.author = author
                news.publish_id = publish_id
                news.body = body
                doc_num += 1
                news.save()
                print("done")


while(1):
    news_crawler()
    time.sleep(60)

sina_rollnews = Articles.objects.filter().values("title").distinct()
print(len(sina_rollnews))