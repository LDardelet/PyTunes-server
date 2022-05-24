from django.urls import path

from library import views

urlpatterns = [
    path('refs/', views.RefListView.as_view(), name='yt refs list'),
    path('refs/<str:yt_id>/', views.RefView.as_view(), name='yt ref'),
    path('musics/', views.MusicListView.as_view(), name='musics list'),
    path('libraries/', views.LibraryListView.as_view(), name='libraries list'),
]
