from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Artist
from .serializers import ArtistSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(response):
    return HttpResponse("<h1> techh! </h1>")

def v1(response):
    return HttpResponse("<h1>view 1</h1>")

@csrf_exempt
def artist_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArtistSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status = 400)

@csrf_exempt
def artist_detail(request,pk):
    try:
        artist= Artist.objects.get(pk=pk)
    
    except Artist.DoeNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArtistSerializer(artist)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArtistSerializer(artist, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status= 400)

    elif request.method == 'DELETE':
        artist.delete()
        return HttpResponse(status=204)

#def artists(request):

#    if request.method not in ('GET', 'POST'):
#        return HttpResponse(status=405)

#    if request.methos == 'GET':
#        artists = ArtistController.get_all_artists()
#        response = [a.serialize() for a in artists]
#        return JSONResponse(response, status=200)