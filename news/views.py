from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import re
import jieba
from .models import Articles,WeiboHot
from django.core.exceptions import ValidationError
from news.inverted_index.search import wordcloud, search

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