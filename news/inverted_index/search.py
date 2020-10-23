import json
import datetime
import time
import re,jieba

import sys,numpy
sys.path.append("/home/ubuntu/xxswl-backend/")
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()

from news.models import Articles

def to_timestamp(strtime:str): ###将字符串时间"2020-05-03 12:01:54"转成时间戳
    timearray = time.strptime(strtime, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(timearray))
    return timestamp

f=open("inverted_index.json",'r',encoding="utf-8")
inverted_index=json.load(f)
stopwords=["记者","责任编辑","标题","报道","京报"]

def search(keyword: str, starttime,endtime):  #热点演进
    ans_list=[]
    dic=inverted_index[keyword]
    L = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    cluster_id=L[0][0]
    sina_rollnews = Articles.objects.filter(cluster_id=cluster_id).order_by("time")
    for article in sina_rollnews:
        text = article.title+article.body
        text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
        seg_word = list(jieba.cut(text))
        ttime=article.time
        if(keyword in seg_word and starttime<to_timestamp(ttime) and to_timestamp(ttime)<endtime):
            print(article.title,article.time)
            ans_list.append({"title":article.title,"time":article.time,"body":article.body})
    return ans_list

anslist=search("美股",1602690735,1602863535)
print(anslist)

def wordcloud(cluster_id,topk):
    word_dic = {}  ####词频
    tfidf_dic = {}
    tot_num=0
    for news in Articles.objects.filter(cluster_id=cluster_id).order_by('-pk'):
        text = news.title + " " + news.body
        text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
        seg_word = list(jieba.cut(text))
        for word in seg_word:
            if (len(word) == 1 or word not in inverted_index.keys() or word in stopwords):
                continue
            if (word in word_dic.keys()):
                word_dic[word] += 1
            else:
                word_dic[word] = 1
            tot_num+=1
        for word in word_dic:
            tfidf_dic[word]=word_dic[word]*numpy.log10(50.0/len(inverted_index[word]))
    L = sorted(tfidf_dic.items(), key=lambda item: item[1], reverse=True)
    L = L[:int(topk)]
    dic = {}
    for l in L:
        dic[l[0].encode("utf-8").decode("utf-8")] = l[1]
    print(dic)
wordcloud(2,30)
print(inverted_index["进行"])