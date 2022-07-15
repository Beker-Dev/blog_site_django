from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'author', 'date', 'category', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    summernote_fields = ('content',)
    list_per_page = 10
    list_filter = ('is_published', 'category', 'author')


admin.site.register(Post, PostAdmin)
