from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import *
from db_model.models import *


class ListBikes(APIView):


    def get(self, request, store_id):
        bikes = Bike.objects.filter(store=store_id)
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)


class DetailBike(APIView):


    def get(self, request, store_id, bike_id):
        bike = Bike.objects.get(pk=bike_id, store=Store.objects.get(pk=store_id))
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data)