from rest_framework import serializers
from .models import Artist, Album, Track

#antes la siguiente linea tenia ModelSerializer
class ArtistSerializerGet(serializers.ModelSerializer):
    #id = serializers.CharField(max_length = 200, primary_key = True)
    #name = serializers.CharField(max_length=100)
    #age = serializers.IntegerField()
    #albums = serializers.URLField(max_length = 200)
    #tracks = serializers.URLField(max_length = 200)
    #self_url = serializers.URLField(max_length = 200)

    class Meta:
        model = Artist
        fields = ['name','age','albums','tracks','self_url']

class ArtistSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'



###

class AlbumSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['name','genre','artist_url','tracks_url','self_url']

class AlbumSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'

####

class TrackSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ['name','duration','times_played','artist_url','album_url','self_url']

class TrackSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__'



    #def create(seld, validated_data):
     #   return Artist.objects.create(validated_data)

    #def update(self,instance, validated_data):
     #   instance.id = validated_data.get('id', instance.id)
     #   instance.name = validated_data.get('name', instance.name)
     #   instance.age = validated_data.get('age', instance.age)
     #   instance.albums = validated_data.get('albums', instance.albums)
     #   instance.tracks = validated_data.get('tracks', instance.tracks)
     #   instance.self_url = validated_data.get('self_url', instance.self_url)
     #   instance.save()
     #   return instance
