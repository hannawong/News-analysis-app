from rest_framework.pagination import PageNumberPagination
class ArticleSearchPageNumberPagination(PageNumberPagination):
    """文章搜索分页器"""
    page_size = 2
    max_page_size = 20
    page_size_query_param = "size"
    page_query_param = "page"
