import json

from django.http import JsonResponse, HttpResponse

from artist.models import Artist

__all__ = (
    'artist_list',
)


def artist_list(request):
    """
    data:{
        'artist' :[
            {
                'melon_id':...,
                'name':...,

        ]
    }
    :param request:
    :return:
    """
    # localhost:8000/api/artist/
    artists = Artist.objects.all()
    data = {
        'artist': [
            {
                'melon_id': artist.melon_id,
                'name': artist.name
            }
            for artist in artists
        ],

    }
    # return HttpResponse(json.dumps(data), content_type='application/json')
    return JsonResponse(data)
