from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=128, null=False)
    body = models.TextField(null=False)
    likes = models.ManyToManyField(User, related_name='like_posts', blank=True)
    tags = models.CharField(max_length=256, null=False)
    hits = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)