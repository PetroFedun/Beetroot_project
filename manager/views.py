from django.shortcuts import render, redirect, get_object_or_404
from .models import Bookmark, Tag
from .forms import BookmarkTagForm, NewUserForm
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')
    
def bookmark_list(request):
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(user=request.user)
        paginator = Paginator(bookmarks, 10)
        tags = Tag.objects.filter(creator=request.user)
        page = request.GET.get('page')
        bookmarks = paginator.get_page(page)
        return render(request, 'bookmark_list.html', {'bookmarks': bookmarks, 'tags': tags})
    else:
        return render(request, 'bookmark_list.html')

def partial_search(request):
    if request.htmx:
        search = request.GET.get('q')
        if search:
            bookmarks = Bookmark.objects.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) | 
                Q(url__icontains=search) | 
                Q(tags__title__icontains=search),
                user=request.user).distinct()          
            tags = Tag.objects.filter(Q(title__icontains=search))
            paginator = Paginator(bookmarks, 10)
            page = request.GET.get('page')
            bookmarks = paginator.get_page(page)
        else:
            bookmarks = Bookmark.objects.filter(user=request.user)
            paginator = Paginator(bookmarks, 10)
            tags = Tag.objects.filter(creator=request.user)
            page = request.GET.get('page')
            bookmarks = paginator.get_page(page)
        return render(request, 'partial_results.html',{'bookmarks': bookmarks, 'tags': tags})

def update(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if request.method == 'POST':
        form = BookmarkTagForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            messages.success(request, "Bookmark updated successfully.")
            return redirect('bookmark_list')
    else:
        form = BookmarkTagForm(instance=bookmark)
    return render(request, 'create.html', {'form': form})

def delete(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if request.method == 'POST':
        bookmark.delete()
        messages.success(request, "Bookmark deleted successfully.")
        return redirect('bookmark_list')
    return render(request, 'delete.html', {'bookmark': bookmark})

def create(request):
    error = ''
    if request.method == 'POST':
        form = BookmarkTagForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False, user=request.user) 
            bookmark.user = request.user
            bookmark.save() 
            tags = form.cleaned_data.get('tags')
            if tags is not None:
                for tag in tags:
                    bookmark.tags.add(tag)
            messages.info(request, "Bookmark created successfully.") 
            return redirect('bookmark_list')
        else:
            error = 'Form isn`t valid'
    else:
        form = BookmarkTagForm()
    data = {
        'is_create_view': True,
        'form': form, 
        'error': error,
    }
    return render(request, 'create.html', data)

def tag_detail(request, tags):
    bookmarks = Bookmark.objects.filter(user=request.user, tags__title=tags) if request.user.is_authenticated else Bookmark.objects.filter(tags__title=tags)
    paginator = Paginator(bookmarks, 10)
    page = request.GET.get('page')
    bookmarks = paginator.get_page(page)
    return render(request, 'tag_detail.html', {'bookmarks': bookmarks, 'tags': tags})

def filter(request):
    selected_tags = request.GET.getlist('tags')
    selected_tags_str = ', '.join(selected_tags)
    bookmarks = Bookmark.objects.filter(user=request.user, tags__title__in=selected_tags)
    paginator = Paginator(bookmarks, 10)
    page = request.GET.get('page')
    bookmarks = paginator.get_page(page)
    context = {
        'bookmarks': bookmarks,
        'tags': selected_tags_str
    }
    return render(request, 'filter.html', context)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("bookmark_list")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request, "register.html", {"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("bookmark_list")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("index")

def profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')

        user = request.user
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'This username is already in use. Please choose a different username.')
            else:
                user.username = new_username
        if new_email:
            if User.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                messages.error(request, 'This email address is already in use. Please use a different email.')
            else: 
                user.email = new_email

        user.save()

        if not messages.get_messages(request):
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  

    return render(request, 'profile.html')

def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.info(request, 'Profile deleted successfully.')
        return redirect('index')
