from django import forms
from blog.models import Post, Comments
from django.forms import ModelForm, Textarea


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'category',
            'title',
            'description',
            'text',
            'image'
        )
        widgets = {
            'text': Textarea(attrs={'rows': 10, 'cols': 100}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'text',
            'author'
        )
        widgets = {
            'text': Textarea(attrs={'rows': 4, 'cols': 40}),
            'author': Textarea(attrs={'rows': 1, 'cols': 20})
        }
