from django.urls import path

from .. import apis

app_name = 'artist'
urlpatterns = [
    path('', apis.ArtistListCreateView.as_view(), name='artist-list'),
    # path('drf/', apis.ArtistListview.as_view(), name='artist-list2'),
    path('<int:pk>/', apis.ArtistListUpdateDestroy.as_view(), name='artist-detail')

]
