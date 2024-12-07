"""
Models
"""
from django.db import models

from django.contrib.auth.models import User

class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    img= models.ImageField(upload_to='images',null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'


class Statistic(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ad_count = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return f'Statistic for {self.author}'