from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("bookmark_manager/", include("bookmark_manager.urls")),
    path("admin/", admin.site.urls),
]
