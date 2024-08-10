from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_purchases", views.my_purchases, name="my_purchases"),
    path("active_biddings", views.active_biddings, name="active_biddings"),
    path("show_listing_categories", views.show_listing_categories, name="show_listing_categories"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("<int:listing_id>/<str:listing_name>", views.show_listing, name="show_listing"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("place_a_bid/<int:listing_id>", views.place_a_bid, name="place_a_bid"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing")

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
