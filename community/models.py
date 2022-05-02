from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=50, unique=True)
    memo = models.TextField(default=None, blank=True, null=True)
    created_by = models.ForeignKey(get_user_model(), default='', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CommunityPost(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), default='', on_delete=models.CASCADE)
    community = models.ForeignKey(Community, default='', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    display = models.IntegerField(blank=True,null=True,default=0)


    def __str__(self):
        return self.content