from django.urls import path

from . import views

urlpatterns = [
    path('refs/', views.RefListView.as_view(), name='yt refs list'),
    path('refs/<str:yt_id>/', views.RefView.as_view(), name='yt ref'),
    path('musics/', views.MusicListView.as_view(), name='musics list'),
    path('musics/<int:music_id>/', views.MusicView.as_view(), name='music'),
    path('musics/<int:music_id>/file/', views.MusicFileView.as_view(), name='music file'),
    path('libraries/', views.LibraryListView.as_view(), name='libraries list'),
    path('library/<int:library_id>/', views.LibraryView.as_view(), name='library'),
    path('profiles/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('clear/', views.TestsCleanerView.as_view(), name='test cleaner')
]
