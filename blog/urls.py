from django.urls import path
from blog.views import blog_list, post_detail, posts_by_categories, search, post_edit, post_delete, \
    post_new, comments_delete

app_name = 'blog'

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('detail/<int:post_pk>/', post_detail, name='post_detail'),
    path('posts_by_categories/<int:category_pk>/', posts_by_categories, name='posts_by_categories'),
    path('search/', search, name='search'),
    path('post_edit/<int:post_pk>/', post_edit, name='post_edit'),
    path('post_new/', post_new, name='post_new'),
    path('post_delete/<int:post_pk>/', post_delete, name='post_delete'),
    path('comments_delete/<int:comment_pk>/', comments_delete, name='comments_delete'),
]