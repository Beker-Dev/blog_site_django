from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from categories.models import Category


class Post(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    excerpt = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    image = models.ImageField(upload_to='post_img/%Y/%m/%d/', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ()
