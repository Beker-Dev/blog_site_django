from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q, Case, Count, When
from .models import Post
from comments.models import Comment, CommentForm
from django.contrib import messages
from django.db import connection


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('category')  # it reduces the number of queries
        qs = qs.filter(is_published=True).order_by('id').reverse()
        qs = qs.annotate(
            total_comments=Count(
                Case(
                    When(
                        comment__is_published=True, then=1
                    )
                )
            )
        )
        return qs


class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')

        if not search:
            return qs
        else:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(author__username__iexact=search) |
                Q(date__icontains=search) |
                Q(category__name__iexact=search) |
                Q(excerpt__icontains=search)
            )
            return qs


class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category')

        if not category:
            return qs
        else:
            qs = qs.filter(category__name__iexact=category)
            return qs


class PostDetail(UpdateView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(is_published=True, post=post.id)
        context['comments'] = comments

        return context

    def form_valid(self, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.post = post

        if self.request.user.is_authenticated:
            comment.user = self.request.user

        comment.save()
        messages.success(self.request, 'Comment sent successfully!')
        return redirect('post_detail', pk=post.id)

