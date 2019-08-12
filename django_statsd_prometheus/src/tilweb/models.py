from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    subject = models.CharField(max_length=160)
    content = models.CharField(max_length=800)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    # We will use the implcit id
    tag = models.CharField(max_length=10, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
