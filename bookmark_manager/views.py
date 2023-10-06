from django.shortcuts import render, redirect
from .models import Bookmark, Tag
from .forms import BookmarkTagForm, NewUserForm
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib import messages

def index(request):
    return render(request, 'index.html')
    
def bookmark_list(request):
    if request.user.is_authenticated:
        user_bookmarks = Bookmark.objects.filter(user=request.user)
        tags = Tag.objects.all()
        return render(request, 'bookmark_list.html', {'bookmarks': user_bookmarks, 'tags': tags})
    else:
        return render(request, 'bookmark_list.html')

def partial_search(request):
    if request.htmx:
      search = request.GET.get('q')
      if search:
          bookmarks = Bookmark.objects.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(url__icontains=search) | Q(tags__title__icontains=search))
          tags = Tag.objects.filter(Q(title__icontains=search))
      else:
          bookmarks = Bookmark.objects.all()
          tags = Tag.objects.all()
      return render(request, 'partial_results.html',{'bookmarks': bookmarks, 'tags': tags})

class BookmarkUpdateView(UpdateView):
    model = Bookmark
    template_name = 'create.html'
    form_class = BookmarkTagForm

class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = '/bookmark_manager/'
    template_name = 'delete.html'

def create(request):
    error = ''
    if request.method == 'POST':
        form = BookmarkTagForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            return redirect('bookmark_list')
        else:
            error = 'Form isn`t valid'
    else:
        form = BookmarkTagForm()
    date = {
        'is_create_view': True,
        'form': form, 
        'error': error,
    }
    return render(request, 'create.html', date)

def tag_detail(request, tag):
    bookmarks = Bookmark.objects.filter(tags__title=tag)
    return render(request, 'tag_detail.html', {'bookmarks': bookmarks, 'tag': tag})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("bookmark_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request, "register.html", {"register_form":form})
