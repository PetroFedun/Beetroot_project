from .models import Bookmark
from django.forms import ModelForm, TextInput

class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['title', 'description', 'url']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum length 50 characters'
            }),
            "description": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum length 200 characters'
            }),
            "url": TextInput(attrs={
                'class': 'form-control',
            }),
        }

