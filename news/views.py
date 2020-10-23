from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import re
import jieba
from .models import Articles,WeiboHot
from django.core.exceptions import ValidationError
f=open("..\\cluster\\inverted_index.json")
inverted_index=json.load(f)
def message(request):
    def gen_response(code: int, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    # GET的完整实现已经给出，同学们无需修改
    if request.method == 'GET':
        limit = request.GET.get('limit', default='100')
        offset = request.GET.get('offset', default='0')
        if not limit.isdigit():
            return gen_response(400, '{} is not a number'.format(limit))
        if not offset.isdigit():
            return gen_response(400, '{} is not a number'.format(offset))
        response= gen_response(200, [
                {
                    'id':msg.id,
                    'title':msg.title.split("@")[0],
                    'hot':msg.hot,
                    'url':msg.title.split("@")[1]
                }
                for msg in WeiboHot.objects.all().order_by('-pk')[int(offset) : int(offset) + int(limit)]
            ])
        return response

def GetWordcloud(request,cluster_id,topk):  ###词云API
    def gen_response(code: int, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)
    if request.method == 'GET':
        word_dic={}  ####词频
        tfidf_dic={}  ####词频* log(all_doc/doc_has_word)
        for news in Articles.objects.filter(cluster_id=cluster_id).order_by('-pk'):
            text=news.title+" "+news.body
            text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
            seg_word = list(jieba.cut(text))
            for word in seg_word:
                if(len(word)==1):
                    continue
                if(word in word_dic.keys()):
                    word_dic[word]+=1
                else:
                    word_dic[word]=1
            for word in word_dic.keys():

        L = sorted(word_dic.items(), key=lambda item: item[1], reverse=True)
        L = L[:int(topk)]
        dic={}
        for l in L:
            dic[l[0].encode("utf-8").decode("utf-8")] = l[1]
        return gen_response(200,dic)
