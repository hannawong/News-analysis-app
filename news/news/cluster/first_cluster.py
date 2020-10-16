##################第一次聚类：将数据库中的文章先聚类一次####################

import jieba
import re
import numpy
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import sys
sys.path.append("/home/ubuntu/xxswl-backend/")
from news.models import Articles

sina_rollnews = Articles.objects.filter()
doc_num=len(sina_rollnews)  #文档总数
print(doc_num,"条新闻")


def jieba_tokenize(text):
    return jieba.lcut(text)
tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize,lowercase=False)
text_list=[]
for article in sina_rollnews:
    text = article.body + article.title + article.title
    text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
    text_list.append(text)

tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)
print("tf_idf===============================")
num_clusters = 20
km_cluster = KMeans(n_clusters=num_clusters, max_iter=10, n_jobs=-1)
result = km_cluster.fit_predict(tfidf_matrix)
f=open("data\\result.txt")
f.write(result)
print(result)