from django.db import models
from web_performance.storage import DomainShardingStorage

class Example1(models.Model):
    file = models.FileField(upload_to='files')

dss = DomainShardingStorage()

class Example2(models.Model):
    file = models.FileField(upload_to='files', storage=dss)