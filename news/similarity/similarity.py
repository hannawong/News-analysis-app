import jieba
import re
import numpy
import json
import sys
sys.path.append("/home/ubuntu/wzh/xxswl-backend/")
sys.path.append("D:\\Program Files\\PycharmProjects\\xxswl-backend")
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()
import sys
sys.path.append("/home/ubuntu/xxswl-backend/")
from news.models import Articles


def Jaccard(grams_A, grams_B):#Jaccard相似度
    temp=0
    for i in grams_A:
        if i in grams_B:
            temp=temp+1
    fenmu=len(grams_A)+len(grams_B)-temp #并集
    jaccard_coefficient=float(temp/fenmu)#交集
    return jaccard_coefficient

def Find_n_sim(id): ####找到和编号为id的文章最接近的n个新闻
    origin_news=Articles.objects.filter(id=id)[0]
    title = re.sub(r"[^\u4e00-\u9fa5]", "", origin_news.body)
    keywords=origin_news.keywords.split("@@@")[0]
    cluster_id=origin_news.cluster_id
    #print(cluster_id)
    gram_A=set(list(jieba.lcut(title))+keywords.split(","))  ###id 的语料集
    #print(gram_A,"======")
    #print(title,keywords)
    sim_dic={}   ###存储相似度
    candidates=Articles.objects.filter(cluster_id=cluster_id).distinct()
    for i in range(0,len(candidates)):
        id=candidates[i].id
        title_i=re.sub(r"[^\u4e00-\u9fa5]", "", candidates[i].body)
        keywords_i=candidates[i].keywords.split("@@@")[0].split(",")
        gram_B=set(list(jieba.lcut(title_i))+keywords_i)
        sim_dic[id]=Jaccard(gram_A,gram_B)
    L = sorted(sim_dic.items(), key=lambda item: item[1], reverse=True)
    sim_ans=""
    for i in range(min(30,len(L))):
        sim_ans+=str(L[i][0])+","
        news=Articles.objects.filter(id=L[i][0])
        #print(news[0].title,news[0].id)
    origin_news.similar_docs=sim_ans
    origin_news.save()

articles=Articles.objects.filter()
print("begin......")
for article in articles:
    id=article.id
    print(id)
    Find_n_sim(id)

