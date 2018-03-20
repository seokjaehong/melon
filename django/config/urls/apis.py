from django.urls import path, include

urlpatterns = [
    path('artist/', include('artist.urls.apis')),
    path('members/', include('members.urls.apis')),
]