from django import forms
from .models import Bookmark, Tag
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookmarkTagForm(forms.ModelForm):
    bookmark_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bookmark Title'}))
    bookmark_description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bookmark Description'}))
    bookmark_url = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bookmark URL'}))
    tag_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag Title'}))

    class Meta:
        model = Bookmark
        fields = []

    def save(self, user, commit=True):
        bookmark_title = self.cleaned_data['bookmark_title']
        bookmark_description = self.cleaned_data['bookmark_description']
        bookmark_url = self.cleaned_data['bookmark_url']
        tag_titles = re.split(r'[,\s]+', self.cleaned_data['tag_title'])
        tags = []
        for tag_title in tag_titles:
            tag, created = Tag.objects.get_or_create(title=tag_title, creator=user)
            tags.append(tag)
        bookmark = Bookmark(title=bookmark_title, description=bookmark_description, url=bookmark_url, user=user)
        bookmark.save()
        bookmark.tags.add(*tags)
        return bookmark

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
