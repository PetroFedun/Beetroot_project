from django.shortcuts import render
from .models import Bookmark

def index(request):
    bookmarks = Bookmark.objects.all()
    return render(request, 'index.html', {'bookmarks': bookmarks})
