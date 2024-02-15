from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("display_specific", views.display_specific, name="display_specific"),
    path("details/<int:id>/<str:title>/", views.details, name="details"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
    path("inactiveListing", views.inactiveListing, name="inactiveListing")
]
