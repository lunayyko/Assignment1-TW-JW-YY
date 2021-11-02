from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

class User(models.Model):
    name         = models.CharField(max_length=40, null=True)
    email        = models.EmailField(max_length=200, unique=True)
    password     = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'

class AccessLog(models.Model):
    user = models.ForeignKey('User', on_delete=SET_NULL, null=True)
    post = models.ForeignKey("posts.Post", on_delete=CASCADE)

    class Meta:
        db_table = 'accesslogs'
        
