####################################建立倒排索引##########################################
import json
import sys,re,jieba
sys.path.append("/home/ubuntu/xxswl-backend/")
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()

from news.models import Articles
sina_rollnews = Articles.objects.filter()

def build_index_cluster():
    ############对于每个聚类构建倒排索引#####################3
    inverted_index = {}  ##{"苹果":{cluster_id1:12,3:23,4:24...},...}
    for article in sina_rollnews:
        # keywords=article.keywords.split(",")
        text = article.body + article.title + article.title
        text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
        seg_word = list(jieba.cut(text))
        cluster_id = article.cluster_id
        for word in seg_word:
            if word not in inverted_index.keys():
                inverted_index[word] = {cluster_id: 1}
            else:
                if cluster_id not in inverted_index[word].keys():
                    inverted_index[word][cluster_id] = 1
                else:
                    inverted_index[word][cluster_id] += 1

    f = open("inverted_index_cluster.json", 'w', encoding="utf-8")
    json.dump(inverted_index, f)

def build_index_article():
    ##############对于每篇文章构建倒排索引###########################
    inverted_index = {}
    for article in sina_rollnews:
        text = article.body + article.title + article.title
        text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
        seg_word = list(jieba.cut(text))
        id = article.id
        for word in seg_word:
            if word not in inverted_index.keys():
                inverted_index[word] = {id: 1}
            else:
                if id not in inverted_index[word].keys():
                    inverted_index[word][id] = 1
                else:
                    inverted_index[word][id] += 1

    f = open("inverted_index_article.json", 'w', encoding="utf-8")
    json.dump(inverted_index, f)

build_index_cluster()
build_index_article()