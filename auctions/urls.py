from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/add", views.add_listing, name="add_listing"),
    path("listing/<str:listing_id>", views.view_listing, name="view_listing"),
    path("listing/<str:listing_id>/bid", views.add_bid, name="add_bid"),
    path("listing/<str:listing_id>/comment", views.add_comment, name="add_comment"),
    path("<str:listing_id>/watchlist/add", views.add_watchlist, name="add_watchlist"),
    path("<str:listing_id>/watchlist/remove", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.view_watchlist , name="view_watchlist"),
    path("categories", views.categories , name="categories"),
    path("category/<str:name>", views.view_category , name="view_category"),
    path("close/<str:listing_id>", views.close_listing , name="close_listing")
    
]
