from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<int:pk>/update/', views.BookmarkUpdateView.as_view(), name='update'),
]
