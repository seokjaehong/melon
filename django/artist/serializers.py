from rest_framework import serializers

from artist.models import Artist, ArtistYouTube

from members.serializers import UserSerializer



class ArtistYouTubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistYouTube
        fields = '__all__'



class ArtistSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(many=True, read_only=True)
    youtube_videos = ArtistYouTubeSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        # fields = (
        #     'name',
        #     'like_users',
        #     'youtube_videos',
        # )
        fields = '__all__'
