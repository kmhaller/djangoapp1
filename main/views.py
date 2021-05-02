from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Artist, Album, Track
from .serializers import ArtistSerializerGet,ArtistSerializerPost,AlbumSerializerGet,AlbumSerializerPost,TrackSerializerGet,TrackSerializerPost
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .controller import ArtistController, AlbumController, TrackController
from .controller import verificar_data_artist_post,verificar_data_album_post, verificar_data_track_post, crear_dict_track
from collections import OrderedDict
# Create your views here.

def index(response):
    return HttpResponse("<h1> techh! </h1>")

def v1(response):
    return HttpResponse("<h1>view 1</h1>")

@api_view(['GET', 'POST'])
def artist_list(request):

    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistSerializerGet(artists, many=True)
        lista = []
        for artist in serializer.data:
            diccionario = artist
            print(diccionario)
            diccionario["self"] = artist["self_url"]
            diccionario.pop("self_url")
            lista.append(diccionario)
        return Response(lista)

    elif request.method == 'POST':
        data = request.data
        print(data)
        verificado = verificar_data_artist_post(data)
        if verificado:
            dic_artista, existe = ArtistController.get_or_create(data["name"], data["age"])
            print(dic_artista)
            
            
            if existe == False: #si no existe
                serializer = ArtistSerializerPost(data=dic_artista)
                if serializer.is_valid():
                    serializer.save()
                    diccionario = serializer.data
                    diccionario["self"] = serializer.data["self_url"]
                    diccionario.pop("self_url")
                    return Response(diccionario, status=status.HTTP_201_CREATED)
                print(serializer.errors)
            elif existe == True:
                serializer = ArtistSerializerGet(dic_artista)
                diccionario = serializer.data
                diccionario["self"] = serializer.data["self_url"]
                diccionario.pop("self_url")
                return Response(diccionario, status=status.HTTP_409_CONFLICT)
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def artist_detail(request,pk):
    try:
        artist= Artist.objects.get(pk=pk)
    
    except Artist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # aca iba el http antes del response

    if request.method == 'GET':
        serializer = ArtistSerializerGet(artist)
        diccionario = serializer.data
        diccionario["self"] = diccionario["self_url"]
        diccionario.pop("self_url")
        return Response(diccionario)

    elif request.method == 'PUT': #si cambia el nombre tiene que cambiar el id
        #verificado = verificar_data_artist_put(request.data)
        #print(verificado)
        #serializer = ArtistSerializerGet(artist, data=request.data)
        #if verificado:
        #    dic_artista, existe = ArtistController.get_or_create(request.data["name"], request.data["age"])
        #    serializer = ArtistSerializerGet(data=dic_artista)
        #    print(dic_artista)
        #    if serializer.is_valid():
        #        serializer.save()
        #        return Response(serializer.data)
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)


    elif request.method == 'DELETE':
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


######     aca parte el Album       #######


@api_view(['GET', 'POST'])
def album_list(request):

    if request.method == 'GET':
        album = Album.objects.all()
        serializer = AlbumSerializerGet(album, many=True)
        lista = []
        for album in serializer.data:
            diccionario = album
            print(diccionario)
            diccionario["artist"] = album["artist_url"]
            diccionario["tracks"] = album["tracks_url"]
            diccionario["self"] = album["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("tracks_url")
            lista.append(diccionario)
        return Response(lista)

    elif request.method == 'POST':
        #data = request.data
        #print(data)
        #verificado = verificar_data_album_post(data) #tiene que tener: nombre, genero, nombre artista
        #if verificado:
        #    dic_album, existe = AlbumController.get_or_create(data["artist_id"], data["name"], data["genre"])
        #    print(dic_album)
            
         #   if existe == False: #si no existe
         #       serializer = AlbumSerializerGet(data=dic_album)
         #       if serializer.is_valid():
         #           serializer.save()
         #           return Response(serializer.data, status=status.HTTP_201_CREATED)
          #  elif existe == True:
          #      serializer = AlbumSerializerGet(dic_album)
          #      return Response(serializer.data, status=status.HTTP_409_CONFLICT)
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'PUT', 'DELETE'])
def album_detail(request,pk):
    try:
        album= Album.objects.get(pk=pk)
    
    except Album.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # aca iba el http antes del response

    if request.method == 'GET':
        serializer = AlbumSerializerGet(album)
        diccionario = serializer.data
        diccionario["artist"] = diccionario["artist_url"]
        diccionario["tracks"] = diccionario["tracks_url"]
        diccionario["self"] = diccionario["self_url"]
        diccionario.pop("self_url")
        diccionario.pop("artist_url")
        diccionario.pop("tracks_url")
        return Response(diccionario)

    elif request.method == 'DELETE':
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    else:
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'POST'])
def artist_detail_albums(request,pk):
    
    
    if request.method == 'GET':

        try:
            artist = Artist.objects.get(pk=pk)
    
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        album = Album.objects.filter(artist=artist)
        serializer = AlbumSerializerGet(album, many=True)
        lista = []
        for album in serializer.data:
            diccionario = album
            print(diccionario)
            diccionario["artist"] = album["artist_url"]
            diccionario["tracks"] = album["tracks_url"]
            diccionario["self"] = album["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("tracks_url")
            lista.append(diccionario)
        return Response(lista)

    elif request.method == 'POST':
        try:
            artist = Artist.objects.get(pk=pk)
    
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        data = request.data
        print(data)
        verificado = verificar_data_album_post(data)
        if verificado:
            dic_album, existe = AlbumController.get_or_create(data["name"], data["genre"], artist, pk)
            print(dic_album)
            if existe == False: #si no existe
                serializer = AlbumSerializerPost(data=dic_album)
                
                if serializer.is_valid():
                    serializer.save()
                    serializer = AlbumSerializerGet(dic_album)
                    diccionario = serializer.data
                    diccionario["artist"] = diccionario["artist_url"]
                    diccionario["tracks"] = diccionario["tracks_url"]
                    diccionario["self"] = diccionario["self_url"]
                    diccionario.pop("self_url")
                    diccionario.pop("artist_url")
                    diccionario.pop("tracks_url")
                    return Response(diccionario, status=status.HTTP_201_CREATED)
                print(serializer.errors)
            elif existe == True:
                serializer = AlbumSerializerGet(dic_album)
                diccionario = serializer.data
                diccionario["artist"] = diccionario["artist_url"]
                diccionario["tracks"] = diccionario["tracks_url"]
                diccionario["self"] = diccionario["self_url"]
                diccionario.pop("self_url")
                diccionario.pop("artist_url")
                diccionario.pop("tracks_url")
                return Response(diccionario, status=status.HTTP_409_CONFLICT)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)


###### aqui parten los tracks #######


@api_view(['GET', 'POST'])
def track_list(request):

    if request.method == 'GET':
        track = Track.objects.all()
        serializer = TrackSerializerGet(track, many=True)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)

    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'PUT', 'DELETE'])
def track_detail(request,pk):
    try:
        track = Track.objects.get(pk=pk)
    
    except Track.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # aca iba el http antes del response

    if request.method == 'GET':
        serializer = TrackSerializerGet(track)
        diccionario = serializer.data
        diccionario["artist"] = diccionario["artist_url"]
        diccionario["album"] = diccionario["album_url"]
        diccionario["self"] = diccionario["self_url"]
        diccionario.pop("self_url")
        diccionario.pop("artist_url")
        diccionario.pop("album_url")
        return Response(diccionario)

    elif request.method == 'DELETE':
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    else:
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
def album_detail_tracks(request,pk):
    
    if request.method == 'GET':
        try:
            album = Album.objects.get(pk=pk)
    
        except Album.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        track = Track.objects.filter(album=album)
        serializer = TrackSerializerGet(track, many=True)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)

    elif request.method == 'POST':
        try:
            album = Album.objects.get(pk=pk)
    
        except Album.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = request.data
        print(data)
        verificado = verificar_data_track_post(data)
        if verificado:
            dic_track, existe = TrackController.get_or_create(data["name"], data["duration"], album, pk)
            print(dic_track)
            if existe == False: #si no existe
                serializer = TrackSerializerPost(data=dic_track)
                
                if serializer.is_valid():
                    serializer.save()
                    serializer = TrackSerializerGet(dic_track)
                    diccionario = serializer.data
                    diccionario["artist"] = diccionario["artist_url"]
                    diccionario["album"] = diccionario["album_url"]
                    diccionario["self"] = diccionario["self_url"]
                    diccionario.pop("self_url")
                    diccionario.pop("artist_url")
                    diccionario.pop("album_url")
                    return Response(diccionario, status=status.HTTP_201_CREATED)
                print(serializer.errors)
            elif existe == True:
                serializer = TrackSerializerGet(dic_track)
                diccionario = serializer.data
                diccionario["artist"] = diccionario["artist_url"]
                diccionario["album"] = diccionario["album_url"]
                diccionario["self"] = diccionario["self_url"]
                diccionario.pop("self_url")
                diccionario.pop("artist_url")
                diccionario.pop("album_url")
                return Response(diccionario, status=status.HTTP_409_CONFLICT)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def artist_detail_tracks(request,pk):
    try:
        artist = Artist.objects.get(pk=pk)
    
    except Artist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        albumes = Album.objects.filter(artist=artist)
        canciones = []
        for album in albumes:
            canciones_album = Track.objects.filter(album = album)
            for cancion in canciones_album:
                canciones.append(cancion)
        print(canciones)
        serializer = TrackSerializerGet(canciones, many=True)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)
    
    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT', 'GET'])
def artist_detail_albums_play(request,pk):
    try:
        artist= Artist.objects.get(pk=pk)
    
    except Artist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # aca iba el http antes del response

    if request.method == 'GET':
        albumes = Album.objects.filter(artist=artist)
        canciones = []
        for album in albumes:
            canciones_album = Track.objects.filter(album = album)
            for cancion in canciones_album:
                canciones.append(cancion)
        print(canciones)
        serializer = TrackSerializerGet(canciones, many=True)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)

    elif request.method == 'PUT': #si cambia el nombre tiene que cambiar el id
        albumes = Album.objects.filter(artist=artist)
        canciones = []
        for album in albumes:
            canciones_album = Track.objects.filter(album = album)
            for song in canciones_album:
                canciones.append(song)
                song.times_played += 1
                diccionario = song.__dict__
                diccionario["album"] = song.album.id
                serializer = TrackSerializerPost(song, data= diccionario)
                if serializer.is_valid():
                    serializer.save()
        print(canciones)
        serializer = TrackSerializerGet(canciones, many=True)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)

    else:
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT', 'GET'])
def album_detail_tracks_play(request,pk):
    try:
        album = Album.objects.get(pk=pk)
    
    except Album.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # aca iba el http antes del response
    
    if request.method == 'GET':
        track = Track.objects.filter(album=album)
        serializer = TrackSerializerGet(track, many=True)
        print(serializer)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)

    elif request.method == 'PUT': #si cambia el nombre tiene que cambiar el id

        canciones_album = Track.objects.filter(album = album)
        print(canciones_album)
        for song in canciones_album:
            print(song)
            song.times_played += 1
            diccionario = song.__dict__
            diccionario["album"] = song.album.id
            serializer = TrackSerializerPost(song, data= diccionario)
            if serializer.is_valid():
                serializer.save()
        track = Track.objects.filter(album=album)
        serializer = TrackSerializerGet(track, many=True)
        lista = []
        for track in serializer.data:
            diccionario = track
            print(diccionario)
            diccionario["artist"] = track["artist_url"]
            diccionario["album"] = track["album_url"]
            diccionario["self"] = track["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            lista.append(diccionario)
        return Response(lista)

    else:
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT', 'GET'])
def track_detail_play(request,pk):
    try:
        track = Track.objects.get(pk=pk)
    
    except Track.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # aca iba el http antes del response

    if request.method == 'GET':
        serializer = TrackSerializerGet(track)
        diccionario = serializer.data
        diccionario["artist"] = diccionario["artist_url"]
        diccionario["album"] = diccionario["album_url"]
        diccionario["self"] = diccionario["self_url"]
        diccionario.pop("self_url")
        diccionario.pop("artist_url")
        diccionario.pop("album_url")
        return Response(diccionario)

    elif request.method == 'PUT': #si cambia el nombre tiene que cambiar el id
        track.times_played += 1
        diccionario = track.__dict__
        diccionario["album"] = track.album.id
        #diccionario.pop('album_id')
        #diccionario.pop('_state')
        #print(diccionario)
        serializer = TrackSerializerPost(track, data= diccionario)  ##### aqui quede ##########
        if serializer.is_valid():
            serializer.save()
            diccionario = serializer.data
            diccionario["artist"] = diccionario["artist_url"]
            diccionario["album"] = diccionario["album_url"]
            diccionario["self"] = diccionario["self_url"]
            diccionario.pop("self_url")
            diccionario.pop("artist_url")
            diccionario.pop("album_url")
            return Response(diccionario)
        print(serializer.errors)
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)



