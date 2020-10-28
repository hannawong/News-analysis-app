import json
import time
import sys
import numpy
sys.path.append("/home/ubuntu/xxswl-backend/")
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()


from news.models import Articles

f=open("news/inverted_index/inverted_index_cluster.json",'r',encoding="utf-8")
f1=open("news/inverted_index/inverted_index_article.json",'r',encoding="utf-8")
inverted_index_cluster=json.load(f)
inverted_index_article=json.load(f1)

cluster_num=50

def to_timestamp(strtime:str): ###将字符串时间"2020-05-03 12:01:54"转成时间戳
    timearray = time.strptime(strtime, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(timearray))
    return timestamp



def search(keyword: str, starttime,endtime):
    #热点演进: 输入关键词，返回和这个关键词有关的新闻列表
    starttime = int(starttime)
    endtime = int(endtime)
    ans_list = []
    if(keyword not in inverted_index_cluster.keys() or keyword not in inverted_index_article.keys()):
        return []
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
            if(len(ans_list) != 0 and article.title == ans_list[-1]["title"]):  ###去重
                continue
            print(article.id, article.cluster_id, article.title, article.time)
            ans_list.append({"title":article.title, "time":to_timestamp(article.time), "body":article.body})
    return ans_list

#anslist=search("新冠",0,16028635350000)


stopwords=["责任编辑","这个","今日","万","亿","一","二","三","四","五","六","七","八","九","十","应当","京报","日","月","就是","因为","自己","现在"]
def stop(str):
    for word in stopwords:
        if word in str:
            return True
    return False

def wordcloud(cluster_id,topk):
    ###########取cluster_id聚类簇里面的关键词；取前topk个tfidf值最大的。
    cluster_id=int(cluster_id)
    topk=int(topk)
    tfidf_dic = {}             ####tfidf值
    for word in inverted_index_cluster.keys():
        if(len(word) == 1 or stop(word)):
            continue
        cluster_freq_dic=inverted_index_cluster[word]  ####这个词语在不同聚类中出现的次数
        if(str(cluster_id) in cluster_freq_dic):  #该词语出现在cluster_id簇中
            if(len(cluster_freq_dic)>=cluster_num/3):
                continue

            tfidf_dic[word]=cluster_freq_dic[str(cluster_id)]*numpy.log2(cluster_num/len(cluster_freq_dic))
    L = sorted(tfidf_dic.items(), key=lambda item: item[1], reverse=True)
    L = L[:topk]
    ans_dic={}
    for l in L:
        ans_dic[l[0]]=int(l[1])
    return ans_dic


#print(wordcloud(19,40))