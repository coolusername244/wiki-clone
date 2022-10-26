from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search_results", views.search, name="search"),
    path("create_entry", views.create, name="create"),
]
