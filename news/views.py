from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import Articles,WeiboHot
from django.core.exceptions import ValidationError

def message(request):
    def gen_response(code: int, data: str):
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
                    'title':msg.title,
                    'hot':msg.hot
                }
                for msg in WeiboHot.objects.all().order_by('-pk')[int(offset) : int(offset) + int(limit)]
            ])
        return response
