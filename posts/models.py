from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from categories.models import Category
from PIL import Image
from django.conf import settings
import os


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image(self.image, 800)

    @staticmethod
    def resize_image(image_name, new_image_width):
        image_path = os.path.join(settings.MEDIA_ROOT, str(image_name))
        image = Image.open(image_path)
        image_width, image_height = image.size

        if image_width <= new_image_width:
            image.close()
        else:
            new_image_height = int((new_image_width * image_height) / image_width)
            new_image = image.resize((new_image_width, new_image_height), Image.ANTIALIAS)
            new_image.save(
                image_path,
                optimize=True,
                quality=60
            )
            new_image.close()
            image.close()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ()
