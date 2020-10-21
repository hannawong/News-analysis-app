##########处理数据库中新加进来的文章，更新IDF_doc_word###########

import jieba
import re
import numpy
import json

import sys
sys.path.append("/home/ubuntu/xxswl-backend/")
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")# project_name 项目名称
django.setup()


from news.models import Articles
sina_rollnews = Articles.objects.filter()
doc_num=len(sina_rollnews)  #文档总数
print(doc_num,"条新闻")
file=open("IDF_doc_word.json",'r',encoding="utf-8")
IDF_doc_word=json.load(file)
for article in sina_rollnews:
    keyword=article.keywords
    if keyword=="null":   #新的文章
        tot_word=0 #文章总词数
        dic_word={} # 文章词语和频率
        text=article.body+article.title+article.title
        text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
        seg_word=list(jieba.cut(text))
        for word in seg_word:
            tot_word+=1
            if(word in dic_word.keys()):
                dic_word[word]+=1
            else:
                dic_word[word]=1
        print(tot_word)
        print(dic_word)
        for word in set(seg_word):
            if(word in IDF_doc_word.keys()):
                IDF_doc_word[word]+=1
            else:
                IDF_doc_word[word]=1
out=open("IDF_doc_word.json",'w',encoding='utf-8')
json.dump(IDF_doc_word,out)


