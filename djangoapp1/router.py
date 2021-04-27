from main.viewsets import ArtistViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('artista', ArtistViewset)