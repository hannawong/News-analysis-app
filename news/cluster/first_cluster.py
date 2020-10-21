##################第一次聚类：将数据库中的文章先聚类一次####################

import jieba
import re
import numpy
import json

import sys
print(sys.path)
sys.path.append("/home/ubuntu/xxswl-backend/")
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import sys
sys.path.append("/home/ubuntu/xxswl-backend/")
from news.models import Articles

sina_rollnews = Articles.objects.filter()
doc_num=len(sina_rollnews)  #文档总数
print(doc_num,"条新闻")


def jieba_tokenize(text):
    return jieba.cut(text)
def cluster():
    tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)
    text_list = []
    for article in sina_rollnews:
        text = article.title+" "+article.keywords+" "+article.body
        text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
        text_list.append(text)

    tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)
    print("tf_idf===============================", tfidf_matrix)
    num_clusters = 100
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=10000, n_init=5)
    result = km_cluster.fit_predict(tfidf_matrix)
    numpy.save("result", result)
    print(result)
cluster()
def assign():
    result = numpy.load("result.npy")
    print(result)
    for i in range(0,len(sina_rollnews)):
        article=sina_rollnews[i]
        print(article.keywords,result[i])
        article.cluster_id=result[i]
        article.save()
assign()