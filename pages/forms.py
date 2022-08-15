from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=40)
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))
    sender = forms.CharField(max_length=40)
    email = forms.EmailField()