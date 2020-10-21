from haystack import indexes
from .models import Articles

class ArticlesIndex(indexes.SearchIndex, indexes.Indexable):
    """
    新闻索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    body = indexes.CharField(model_attr='body')

    def get_model(self):
        """返回建立索引的模型类"""
        return Articles

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        # return self.get_model().objects.filter(is_launched=True)
        return self.get_model().objects.all()
