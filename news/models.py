from django.db import models
# Create your models here.
class Articles(models.Model):
    url=models.CharField(max_length=100)
    title=models.CharField(max_length=60)
    time=models.CharField(max_length=15)
    author=models.CharField(max_length=15)
    body=models.CharField(max_length=1000)
    keywords=models.CharField(max_length=300,default="null")  # 地点筛选后may存下来，@ 分割，记在后方 因为聚类可能会变化

    cluster_id=models.IntegerField(default=-1)
    emotion=models.FloatField(default=0.0)


class WeiboHot(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=300)
    hot=models.IntegerField()

    def __str__(self):
        return self.url+self.title+str(self.time)


class WeiboSocialEvents(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=300)