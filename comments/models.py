from django.db import models
from django import forms
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone
import requests


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
        raw_data = self.data
        recaptcha_client_response = self.data.get('g-recaptcha-response')

        if not recaptcha_client_response:
            self.add_error(
                'comment',
                'Error: Recaptcha is needed!'
            )
        else:

            recaptcha_server_response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': '6LfN3P4gAAAAAFajeQA6w0a8WHhkxpazyzWRbU_J',
                    'response': recaptcha_client_response
                }
            ).json()

            if not recaptcha_server_response.get('success'):
                self.add_error(
                    'comment',
                    'Error: Invalid Recaptcha'
                )
            else:
                cleaned_data = self.cleaned_data
                name = cleaned_data.get('name')
                comment = cleaned_data.get('comment')

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




