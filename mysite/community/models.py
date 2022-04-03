from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Community(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(get_user_model(), default='', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
