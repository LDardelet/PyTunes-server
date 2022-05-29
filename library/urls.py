from django.urls import path

from . import views

urlpatterns = [
    path('refs/', views.RefListView.as_view(), name='yt refs list'),
    path('refs/<str:yt_id>/', views.RefView.as_view(), name='yt ref'),
    path('musics/', views.MusicListView.as_view(), name='musics list'),
    path('musics/<int:music_id>/', views.MusicView.as_view(), name='music'),
    path('musics/<int:music_id>/file/', views.MusicFileView.as_view(), name='music file'),
    path('playlist/', views.PlaylistsListView.as_view(), name='playlists list'),
    path('playlist/<int:playlist_id>/', views.PlaylistView.as_view(), name='playlist details'),
    path('profiles/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('clear/', views.TestsCleanerView.as_view(), name='test cleaner')
]
