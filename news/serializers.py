from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ArticlesIndex

class ArticleIndexSerializer(HaystackSerializer):
    """
    文章索引结果数据序列化器
    """
    class Meta:
        index_classes = [ArticlesIndex]
        fields = ('text', 'title', 'author', 'body')
