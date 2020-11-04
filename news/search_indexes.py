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
    url = indexes.CharField(model_attr='url')
    time = indexes.DateTimeField(model_attr='time')
    keywords = indexes.CharField(model_attr='keywords')
    cluster_id = indexes.IntegerField(model_attr='cluster_id')
    emotion = indexes.FloatField(model_attr='emotion')

    def get_model(self):
        """返回建立索引的模型类"""
        return Articles

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        # return self.get_model().objects.filter(is_launched=True)
        return self.get_model().objects.all()

    # def prepare_time(self, obj):
    #     timearray = time.strptime(obj.time, '%Y-%m-%d %H:%M:%S')
    #     timestamp = int(time.mktime(timearray))
    #     return timestamp