from django.db import models

# Create your models here.
class HeatMapData(models.Model):
    date=models.DateTimeField()  #??
    cluster_id=models.IntegerField(default=-1)
    data=models.CharField(max_length=1000) #my json
