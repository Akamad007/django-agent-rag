from django.contrib import admin
from django.urls import path

from demo_app.views import ask_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ask/", ask_view),
]

