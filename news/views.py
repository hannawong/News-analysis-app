from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import re
import jieba
from .models import Articles,WeiboHot
from django.core.exceptions import ValidationError
from news.inverted_index.search import wordcloud, search
from elasticsearch import Elasticsearch


def message(request):
    def gen_response(code: int, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)
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
        dic=wordcloud(cluster_id,topk)
        return gen_response(200,dic)


def GetTimeline(request, keyword, starttime, endtime):
    def gen_response(code: int, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)
    if request.method == 'GET':
        news_list=search(keyword, starttime, endtime)
        return gen_response(200,news_list)

def searchNews(request):
    def gen_response(code: int, data: str):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)
    if request.method == 'GET':
        q = request.GET.get('q', default='a')
        time_from = request.GET.get('from')
        time_to = request.GET.get('to')
        print(q, time_from, time_to)
        if time_from and time_to:
            print(1)
            q_body={
                "query":{
                    "bool":{
                        "must":[
                        {
                            "match":{
                                "text":q
                            }
                        },{
                            "range": {
                                "time": {
                                    "gt": time_from,
                                    "lte": time_to
                                }
                            }
                        }],
                        "must_not":[],
                        "should":[]
                    }
                },
                "from":0,
                "size":10,
                "sort":[],
                "aggs":{}
            }
        elif time_from:
            print(2)
            q_body={
                "query":{
                    "bool":{
                        "must":[
                        {
                            "match":{
                                "text":q
                            }
                        },{
                            "range": {
                                "time": {
                                    "gt": time_from
                                }
                            }
                        }],
                        "must_not":[],
                        "should":[]
                    }
                },
                "from":0,
                "size":10,
                "sort":[],
                "aggs":{}
            }
        elif time_to:
            print(3)
            q_body={
                "query":{
                    "bool":{
                        "must":[
                        {
                            "match":{
                                "text":q
                            }
                        },{
                            "range": {
                                "time": {
                                    "lte": time_to
                                }
                            }
                        }],
                        "must_not":[],
                        "should":[]
                    }
                },
                "from":0,
                "size":10,
                "sort":[],
                "aggs":{}
            }
        else:
            print(4)
            q_body={
                "query":{
                    "bool":{
                        "must":[{
                            "match":{
                                "text":q
                            }}],
                        "must_not":[],
                        "should":[]
                    }
                },
                "from":0,
                "size":10,
                "sort":[],
                "aggs":{}
            }

    es = Elasticsearch()

    response = es.search(
        index="xxswl",
        body=q_body
    )

    # for hit in response['hits']['hits']:
    #    print(hit['_score'], hit['_source']['text'])

    response = gen_response(200, response['hits']['hits'])
    return response