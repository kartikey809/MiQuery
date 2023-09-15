from datetime import *
from django.utils import timezone
from django.db import models

# Create your models here.
class Results(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=100,null=True)
    usecase = models.CharField(max_length=100,null=True)
    description = models.TextField(max_length=100,null=True)
    code = models.TextField(null=True) 
    copy_count = models.BigIntegerField(default=0)
    view_count = models.BigIntegerField(default=0)
    upvote = models.BigIntegerField(default=0)
    Isobsolete = models.BooleanField(default=False)
    author = models.CharField(max_length=30,null=True)
    language = models.CharField(max_length=10,null=True)
    explain = models.TextField(null=True) 
    uploadedon = models.DateField(default=timezone.now())

    
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        super(Results , self).save(*args,**kwargs)




