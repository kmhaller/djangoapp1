from base64 import b64encode
from .models import Artist, Album, Track

HOST = 'https://salty-shore-90769.herokuapp.com'

def encode(nombre, segundo_param = None):
    if segundo_param == None:
        encoded = b64encode(nombre.encode()).decode('utf-8')
    else:
        string = nombre + ":" + segundo_param
        encoded = b64encode(string.encode()).decode('utf-8')
    return encoded[0:22]

def verificar_data_artist_post(data):
    if len(data.keys()) == 2 and ("name" and "age" in data.keys()) and type(data["name"]) == str and type(data["age"]) == int:
        return True

def verificar_data_artist_put(data):
    if len(data.keys()) == 6 and ("name" and "age" in data.keys()) and type(data["name"]) == str and type(data["age"]) == int:
        return True

class ArtistController():

    @classmethod
    def get_artist(self, artist_id):
        try:
            artist= Artist.objects.get(id=artist_id)
            if artist != None:
                return artist
    
        except Artist.DoesNotExist:
            return False

    @classmethod
    def get_or_create(self, name, age):
        artist_id = encode(str(name))
        artista_existente = self.get_artist(artist_id)
        if artista_existente == False: #si no existe
            dic_artista = {}
            dic_artista["id"] = artist_id
            dic_artista["name"] = str(name)
            dic_artista["age"] = age
            dic_artista["albums"] = f"{HOST}/artists/{artist_id}/albums"
            dic_artista["tracks"] = f"{HOST}/artists/{artist_id}/tracks"
            dic_artista["self_url"] = f"{HOST}/artists/{artist_id}"
            
            return dic_artista, False
        return artista_existente, True
    


def verificar_data_album_post(data):
    if len(data.keys()) == 2 and ("name" and "genre" in data.keys()) and type(data["name"]) == str and type(data["genre"]) == str:
        return True
            

class AlbumController():

    @classmethod
    def get_album(self, album_id):
        try:
            album= Album.objects.get(id=album_id)
            if album != None:
                return album
    
        except Album.DoesNotExist:
            return False

    @classmethod
    def get_or_create(self, name, genre, artista, id_artista):
        album_id = encode(str(name), id_artista)
        album_existente = self.get_album(album_id)
        if album_existente == False: #si no existe
            dic_album = {}
            dic_album["id"] = album_id
            dic_album["name"] = str(name)
            dic_album["artist"] = artista.id
            dic_album["genre"] = genre
            dic_album["artist_url"] = f"{HOST}/artists/{id_artista}"
            dic_album["tracks_url"] = f"{HOST}/albums/{album_id}/tracks"
            dic_album["self_url"] = f"{HOST}/albums/{album_id}"
            
            return dic_album, False
        return album_existente, True


def verificar_data_track_post(data):
    if len(data.keys()) == 2 and ("name" and "duration" in data.keys()) and type(data["name"]) == str and type(data["duration"]) == float:
        return True
            

class TrackController():

    @classmethod
    def get_track(self, track_id):
        try:
            track = Track.objects.get(id=track_id)
            if track != None:
                return track
    
        except Track.DoesNotExist:
            return False

    @classmethod
    def get_or_create(self, name, duration, album, id_album):
        track_id = encode(str(name), id_album)
        track_existente = self.get_track(track_id)
        if track_existente == False: #si no existe
            dic_track = {}
            dic_track["id"] = track_id
            dic_track["album"] = album.id
            dic_track["name"] = str(name)
            dic_track["duration"] = duration
            dic_track["times_played"] = 0
            dic_track["artist_url"] = f"{HOST}/artists/{album.artist.id}"
            dic_track["album_url"] = f"{HOST}/albums/{id_album}"
            dic_track["self_url"] = f"{HOST}/tracks/{track_id}"
            
            return dic_track, False
        return track_existente, True
    
def crear_dict_track(track):
    dic_track = {}
    dic_track["id"] = track.id
    dic_track["album"] = track.album ### no esta funcionando entregar el obe¡jeto ver por que!!! #####
    dic_track["name"] = track.name
    dic_track["duration"] = track.duration
    dic_track["times_played"] = track.times_played
    dic_track["artist_url"] = f"{HOST}/artists/{track.album.artist.id}"
    dic_track["album_url"] = f"{HOST}/albums/{track.album.id}"
    dic_track["self_url"] = f"{HOST}/tracks/{track.id}"
    return dic_track