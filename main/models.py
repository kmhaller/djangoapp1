from django.db import models

# Create your models here.

class Artist(models.Model):
    id = models.CharField(max_length = 200, primary_key = True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    albums = models.URLField(max_length = 200)
    tracks = models.URLField(max_length = 200)
    self_url = models.URLField(max_length = 200)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    id = models.CharField(max_length = 200, primary_key = True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length= 200)
    genre = models.CharField(max_length=200)
    artist_url = models.URLField(max_length = 200)
    tracks_url = models.URLField(max_length = 200)
    self_url = models.URLField(max_length = 200)

    def __str__(self):
        return self.name
    
class Track(models.Model):
    id = models.CharField(max_length = 200, primary_key = True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length= 200)
    duration = models.FloatField(max_length=200)
    times_played = models.IntegerField()
    artist_url = models.URLField(max_length = 200)
    album_url = models.URLField(max_length = 200)
    self_url = models.URLField(max_length = 200)

    def __str__(self):
        return self.name

#tamo