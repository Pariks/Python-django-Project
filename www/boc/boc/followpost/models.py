from django.db import models
from django.utils import timezone
from news.models import Article
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class FollowPostItem(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    date_commented = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article)
    comment_replies = models.ForeignKey('self', null=True)
    child = models.IntegerField(default=1)
    def __unicode__(self):
        return self.content


class Comments(MPTTModel):
    article = models.ForeignKey(Article)
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    class MPTTMeta:
        order_insertion_by = ['article']
    def __unicode__(self):
        return self.content
