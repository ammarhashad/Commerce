from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("All", views.All, name="All"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:item_id>/<int:watch>", views.item, name="item"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("close/<int:item_id>", views.close, name="close"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("watchlist/<int:item_id>/<int:value>",views.watchlist_controll,name="watchlist_controll"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:name>", views.category, name="category"),
    path("your/item", views.my_item, name="my_item"),
]
