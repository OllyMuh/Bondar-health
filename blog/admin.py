from django import forms
from django.contrib import admin

from blog.models import Category, Post, Comments

# from ckeditor_uploader.widgets import CKEditorUploadingWidget
#
#
# class PostAdminForm(forms.ModelForm):
#     text = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Post
#         fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    list_display = [
        'category', 'title',
        'published'
    ]
    list_filter = [
        'published',
        'category']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'published_date',
        'author'
    ]
