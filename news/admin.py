"""
"""
from django.contrib import admin
import sys
from news import models

#Register models
admin.site.register(models.Articles)