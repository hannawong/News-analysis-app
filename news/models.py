from django.db import models
# Create your models here.
class Articles(models.Model):
    url=models.CharField(max_length=100)
    title=models.CharField(max_length=60)
    time=models.DateTimeField()
    author=models.CharField(max_length=30)
    publish_id=models.CharField(max_length=30)
    body=models.CharField(max_length=3000)
    def __str__(self):
        return self.url+self.title+str(self.time)