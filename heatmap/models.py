from django.db import models

# Create your models here.
class HeatMapData(models.Model):
    time=models.CharField(max_length=15,default="null")
    cluster_id=models.IntegerField(default=-1)
    locdict=models.CharField(max_length=2000,default="null") #my json
