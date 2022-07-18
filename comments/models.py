from django.db import models
from django import forms
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)


class CommentForm(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data
        name = data.get('name')
        comment = data.get('comment')

        if len(name) < 4:
            self.add_error(
                'name',
                'Error: Name needs 5 characters at least!'
            )

        if len(comment) < 10:
            self.add_error(
                'comment',
                'Error: Comment needs 10 characters at least!'
            )

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')




