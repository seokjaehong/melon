from django.urls import path, include
from django.contrib import admin

from ..views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    # artist/로 시작하는 path가
    # artist.urls모듈을 include하도록 설정
    path('', index, name='index'),
    path('', include('members.urls.views')),

    path('artist/', include('artist.urls.views')),
    path('album/', include('album.urls')),
    path('song/', include('song.urls')),


]