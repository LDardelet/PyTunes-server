from django.urls import path

from . import views 

urlpatterns = [
        path('<int:playlist_id>/', views.PlaylistView.as_view(), name='playlist management'),
]
