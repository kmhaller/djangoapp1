from rest_framework import viewsets
from . import models
from . import serializers

class ArtistViewset(viewsets.ModelViewSet):
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializerGet
