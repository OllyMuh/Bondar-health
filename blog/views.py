from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import CreateView

from blog.forms import PostForm, CommentForm
from blog.models import Category, Post, Comments


def blog_list(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    # now = timezone.now()
    # month_ago = now - timedelta(weeks=4)
    # latest_posts = Post.objects.filter(published__gte=month_ago).order_by('-published').distinct()[:5]
    context = {
        'categories': categories,
        'posts': posts,
        # 'latest_posts': latest_posts,
        'page': page,
    }
    return render(
        request,
        'blog/blog.html',
        context
    )


def post_detail(request, post_pk):
    post = Post.objects.filter(pk=post_pk).first()
    comments = Comments.objects.filter(post__pk=post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.published_date = timezone.now()
            comment.save()
            return redirect('blog:post_detail', post_pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post_detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'comment_form': comment_form,
                  })


# filter posts by categories

def posts_by_categories(request, category_pk):
    posts = Post.objects.all().filter(category__pk=category_pk)
    categories = Category.objects.all()
    paginator = Paginator(posts, 5)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    context = {
        'categories': categories,
        'posts': posts,
        'page': page,
    }
    return render(
        request,
        'blog/blog.html',
        context
    )

# Search for posts


def search(request):
    subject = request.GET.get('subject')
    posts_search = Post.objects.filter(
                                 Q(title__icontains=subject) |
                                 Q(description__icontains=subject) |
                                 Q(text__icontains=subject)
    )
    paginator = Paginator(posts_search, 5)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    context = {
        'subject': subject,
        'posts_search': posts_search,
        'page': page,
    }
    return render(request, 'blog/search.html', context)


# New post

def post_new(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)                         # added request.FILES to load files
        if post_form.is_valid():
            post = post_form.save()
            # post.published = timezone.now()
            post.save()
            return redirect('blog:post_detail', post_pk=post.pk)
    else:
        post_form = PostForm()
        return render(request, 'blog/post_edit.html', {'post_form': post_form})


# Edit posts

def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        post_form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'post_form': post_form})
    else:
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.save()
            return redirect('blog:post_detail', post_pk=post.pk)


# Кнопка удалить публикацию
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk).delete()
    return redirect('blog:blog_list')


# Comments delete
def comments_delete(request, post_pk, comment_pk):
    post = Post.objects.get(pk=post_pk)
    comment = get_object_or_404(Comments, pk=comment_pk).delete()
    return redirect("blog:post_detail", post_pk=post.pk)
