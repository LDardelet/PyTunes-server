from django.urls import path

from library import views

urlpatterns = [
    path('refs/', views.RefListView.as_view(), name='yt refs list'),
    path('musics/', views.MusicListView.as_view(), name='musics list'),
    path('libraries/', views.LibraryListView.as_view(), name='libraries list'),
]
