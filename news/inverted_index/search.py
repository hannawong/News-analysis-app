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

f=open("inverted_index_cluster.json",'r',encoding="utf-8")
f1=open("inverted_index_article.json",'r',encoding="utf-8")
inverted_index_cluster=json.load(f)
inverted_index_article=json.load(f1)

def to_timestamp(strtime:str): ###将字符串时间"2020-05-03 12:01:54"转成时间戳
    timearray = time.strptime(strtime, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(timearray))
    return timestamp

def search(keyword: str, starttime,endtime):
    #热点演进: 输入关键词，返回和这个关键词有关的新闻列表
    ans_list = []
    dic_cluster = inverted_index_cluster[keyword]
    dic_article = inverted_index_article[keyword]
    print(dic_article)
    L = sorted(dic_cluster.items(), key = lambda item: item[1], reverse = True)
    cluster_id = L[0][0]  ###找到最相关的一个聚类
    sina_rollnews = Articles.objects.filter(cluster_id = cluster_id).order_by("time")
    for article in sina_rollnews:
        if str(article.id) not in dic_article.keys() or dic_article[str(article.id)] <= 3:  #查倒排索引，找到含有三个以上这个关键词的文档
            continue
        ttime = article.time
        if(starttime<to_timestamp(ttime) and to_timestamp(ttime)<endtime):  #时间比对
            print(article.id,article.cluster_id,article.title, article.time)
            ans_list.append({"title":article.title, "time":to_timestamp(article.time), "body":article.body})
    return ans_list

anslist=search("疫苗",0,16028635350000)
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