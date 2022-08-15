from django import forms
from .models import Review
from django.forms import ModelForm, Textarea


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = (
            'text',
            'rating',
        )
        widgets = {
            'text': Textarea(attrs={'class': 'form-control shadow px-2', 'rows': 6}),
            'rating': forms.RadioSelect
        }