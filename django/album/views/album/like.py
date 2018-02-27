from django.shortcuts import redirect

from ...models import Album

__all__ = (
    'album_like_toggle',
)


def album_like_toggle(request, album_pk):
    album = Album.objects.get(pk=album_pk)
    if request.method == 'POST':
        album.toggle_like_user(user=request.user)
        next_path = request.POST.get('next-path', 'album:album-list')
        return redirect(next_path)
