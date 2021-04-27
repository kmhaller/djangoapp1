from rest_framework import serializers
from .models import Artist

#antes la siguiente linea tenia ModelSerializer
class ArtistSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(max_length = 200, primary_key = True)
    #name = serializers.CharField(max_length=100)
    #age = serializers.IntegerField()
    #albums = serializers.URLField(max_length = 200)
    #tracks = serializers.URLField(max_length = 200)
    #self_url = serializers.URLField(max_length = 200)

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

    class Meta:
        model = Artist
        fields = '__all__'

