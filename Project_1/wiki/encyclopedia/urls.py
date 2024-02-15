from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.get_page, name="greet"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("random/", views.random_page, name="random")
]
