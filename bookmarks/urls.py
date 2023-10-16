from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("manager/", include("manager.urls")),
    path("admin/", admin.site.urls),
]
