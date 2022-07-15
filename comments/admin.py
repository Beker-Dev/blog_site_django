from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'post', 'user', 'date', 'is_published')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'post', 'user')
    list_per_page = 10


admin.site.register(Comment, CommentAdmin)
