from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), default='', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    display = models.IntegerField(blank=True,null=True,default=0)

    def __str__(self):
        return self.content

    
