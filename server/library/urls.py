from django.urls import path

from library import views

urlpatterns = [
    path('musics/', views.MusicListView.as_view(), name='musics list'),
    path('libraries/', views.LibraryListView.as_view(), name='libraries list'),
]
