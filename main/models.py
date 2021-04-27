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