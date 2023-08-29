from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.display, name="display"),
    path("newpage/", views.newPage, name="newPage"),
    path("random/", views.randomPage, name="randomPage"),
    path("search/", views.searchbar, name="searchbar"),
    path("error/", views.newPage, name="error" ),
    path("edit/<str:titles>/",views.edit, name="edit")
]
