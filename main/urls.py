from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name= "index"),
    path('artists', views.artist_list),
    path('artists/<str:pk>', views.artist_detail),

    path('albums', views.album_list),
    path('albums/<str:pk>', views.album_detail),
    
    path('tracks', views.track_list),
    path('tracks/<str:pk>', views.track_detail),
    
    path('artists/<str:pk>/albums', views.artist_detail_albums),
    path('artists/<str:pk>/tracks', views.artist_detail_tracks),
    path('albums/<str:pk>/tracks', views.album_detail_tracks),

    path('tracks/<str:pk>/play', views.track_detail_play),
    path('artists/<str:pk>/albums/play', views.artist_detail_albums_play),
    path('albums/<str:pk>/tracks/play', views.album_detail_tracks_play)
    
]