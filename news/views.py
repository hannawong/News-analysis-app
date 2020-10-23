from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import Articles,WeiboHot
from django.core.exceptions import ValidationError
# from drf_haystack.viewsets import HaystackViewSet
# from .serializers import ArticleIndexSerializer
# from .paginations import ArticleSearchPageNumberPagination
# from haystack.views import SearchView as _SearchView
# from haystack.generic_views import SearchView
from elasticsearch import Elasticsearch


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

def search(request):
    def gen_response(code: int, data: str):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)
    if request.method == 'GET':
        q = request.GET.get('q', default='a')

    client = Elasticsearch()

    response = client.search(
        index="xxswl",
        body={"query":{"bool":{"must":[{"match":{"text":q}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
    )

    print("1\n")
    for hit in response['hits']['hits']:
        print(hit['_score'], hit['_source']['text'])

    response = gen_response(200, response['hits']['hits'])
    return response


# class ArticleSearchViewSet(HaystackViewSet):
#     """
#     文章搜索
#     """

#     index_models = [Articles]

#     serializer_class = ArticleIndexSerializer
#     pagination_class = ArticleSearchPageNumberPagination



# 搜索文章
# class SearchArticleViewSet(HaystackViewSet):
#     # GET  /Headlines/search/?text=<搜索关键字>
#     # 这里可以写多个模型，相应的：serializer里也可以写多个index_classes
#     index_models = [Article]
#     serializer_class = SearchArticleIndexSerializer



# class ArticleSearchViewSet(_SearchView):
#     # 模版文件
#     # template = 'news/search.html'
#     {"query":{"bool":{"must":[{"match":{"text":"a"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}


#     # 重写响应方式，如果请求参数q为空，返回模型News的热门新闻数据，否则根据参数q搜索相关数据
#     def create_response(self):
#         kw = self.request.GET.get('q', '')
#         if not kw:
#             # 如果没有索引值,就全部搜索出来
#             show_all = True
#             news = Articles.objects.all()

#             # paginator = Paginator(hot_news, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
#             paginator = ArticleSearchPageNumberPagination
#             try:
#                 page = paginator.page(int(self.request.GET.get('page', 1)))
#             except PageNotAnInteger:
#                 # 如果参数page的数据类型不是整型，则返回第一页数据
#                 page = paginator.page(1)
#             except EmptyPage:
#                 # 用户访问的页数大于实际页数，则返回最后一页的数据
#                 page = paginator.page(paginator.num_pages)
#             return render(self.request, self.template, locals())
#         else:
#             show_all = False
#             qs = super(_SearchView, self).create_response()
#             return qs
#     pass
