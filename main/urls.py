from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name= "index"),
    path('artists', views.artist_list),
    path('artists/<int:pk>', views.artist_detail)
    #path("artists", views.artists, name= "all_artists"),
    #path("artists/<artist_id>", views.artist_detail, name= "artist_by_id"),
]