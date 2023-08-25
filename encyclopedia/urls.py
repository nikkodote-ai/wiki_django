from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("random", views.random_page, name="random_page"),
    path("wiki/<str:title>/edit_page", views.edit_entry, name="edit_entry"),
    path("create_new_page", views.new_entry, name="new_entry"),
    path("search", views.search, name="search"),
]
