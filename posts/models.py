from django.db import models
from django.db.models.deletion import CASCADE

from core.models import TimeStamp

class Post(TimeStamp):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    viewcount = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=CASCADE)

    class Meta:
        db_table = 'posts'

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'


class Comment(TimeStamp):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    class Meta:
        db_table = 'comments'