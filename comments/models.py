from django.db import models
from django import forms
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='Title')
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ()
