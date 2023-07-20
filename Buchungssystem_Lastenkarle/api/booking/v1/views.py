from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import *
from db_model.models import *


class ListRegion(APIView):


    def get(self, request):
        region = Store.REGION
        serializer = RegionSerializer(region, many=True)
        return Response(serializer.data)


class ListBikes(APIView):

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)


class DetailBike(APIView):

    def get_Bike(self, bike_id):
        try:
            return Bike.objects.get(pk=bike_id)
        except Bike.DoesNotExist:
            raise Http404

    def get(self, request, bike_id):
        bike = self.get_Bike(bike_id)
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data)


class ListStores(APIView):

    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


class DetailStore(APIView):

    def get(self, request, bike_id):
        bike = Bike.objects.get(pk=bike_id)
        store = bike.store
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data)


class ListAvailabilities(APIView):

    def get(self, request):
        availabilities = Availability_Status.objects.all()
        serializer = Availability_StatusSerializer(availabilities, many=True)
        return Response(serializer.data)


class DetailBikeAvailability(APIView):


    def get(self, request, bike_id):
        availabilities_of_bike = Availability_Status.objects.filter(availability__bike=bike_id)
        serializer = Availability_StatusSerializer(availabilities_of_bike, many=True)
        return Response(serializer.data)


class DetailBooking(APIView):


    def post(self, request, bike_id):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)