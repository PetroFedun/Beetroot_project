from django.shortcuts import render, redirect
from .models import Bookmark
from .forms import BookmarkForm

def index(request):
    bookmarks = Bookmark.objects.all()
    return render(request, 'index.html', {'bookmarks': bookmarks})

def create(request):
    error = ''
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = 'Form isn`t valid'
    form = BookmarkForm()
    date = {
        'form': form,
        'error': error
    }
    return render(request, 'create.html', date)
