from django.db import models
# Create your models here.
class Articles(models.Model):
    url=models.CharField(max_length=100)
    title=models.CharField(max_length=60)
    time=models.DateTimeField()
    author=models.CharField(max_length=15)
    body=models.CharField(max_length=1000)
    keywords=models.CharField(max_length=100,default="null")
    cluster_id=models.IntegerField(default=-1)

class WeiboHot(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=100)
    hot=models.IntegerField()

    def __str__(self):
        return self.url+self.title+str(self.time)