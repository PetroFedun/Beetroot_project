from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bookmark_list', views.bookmark_list, name='bookmark_list'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('partial-search/', views.partial_search, name='partial_search'),
    path('tag/<str:tag>/', views.tag_detail, name='tag_detail'),
    path('filter/', views.filter, name='filter'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]
