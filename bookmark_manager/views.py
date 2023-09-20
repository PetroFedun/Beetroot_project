from django.shortcuts import render, redirect
from .models import Bookmark
from .forms import BookmarkForm
from django.views.generic import UpdateView

def index(request):
    bookmarks = Bookmark.objects.all()
    return render(request, 'index.html', {'bookmarks': bookmarks})

class BookmarkUpdateView(UpdateView):
    model = Bookmark
    template_name = 'create.html'
    form_class = BookmarkForm

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
        'is_create_view': True,
        'form': form, 
        'error': error, 
    }
    return render(request, 'create.html', date)
