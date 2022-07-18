from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'),
    path('categories/<str:category>/', views.PostCategory.as_view(), name='post_category'),
    path('search/', views.PostSearch.as_view(), name='post_search'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
]
