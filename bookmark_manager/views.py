from django.shortcuts import render, redirect
from .models import Bookmark
from .forms import BookmarkForm
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q

def index(request):
    bookmarks = Bookmark.objects.all()
    return render(request, 'index.html', {'bookmarks': bookmarks})

def partial_search(request):
    if request.htmx:
      search = request.GET.get('q')
      if search:
          bookmarks = Bookmark.objects.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(url__icontains=search))
      else:
          bookmarks = Bookmark.objects.all()
      return render(request, 'partial_results.html',{'bookmarks': bookmarks})

class BookmarkUpdateView(UpdateView):
    model = Bookmark
    template_name = 'create.html'
    form_class = BookmarkForm

class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = '/bookmark_manager/'
    template_name = 'delete.html'

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
