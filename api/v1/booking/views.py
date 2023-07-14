from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import *
from db_model import *


class ListRegion(APIView):

    def get(self, request, format=None):
        region = Store.REGION
        serializer = RegionSerializer(region, many=True)
        return Response(serializer.data)


class ListBikes(APIView):

    def get(self, request, format=None):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)


class DetailBike(APIView):


    def get_Bike(self, pk):
        try:
            return Bike.objects.get(pk=pk)
        except Bike.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        bike = self.get_Bike(pk)
        serializer = BikeSerializer(bike)
        return Response(serializer.data)


class ListStores(APIView):

    def get(self, request, format=None):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


class DetailStore(APIView):


    def get_Store(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        store = self.get_Store(pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data)


class ListAvailabilities(APIView):


    def get(self, request):
        availability = Availability.objects.all()
        serializer = Availability_Serializer(availability)
        return Response(serializer.data)


    def get_Store(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise Http404


class DetailAvailability(APIView):


    def get_Bike(self, pk):
        try:
            return Bike.objects.get(pk=pk)
        except Bike.DoesNotExist:
            raise Http404


    def get(self, request, pk_bike):
        bike = Bike.objects.get(pk=pk_bike)
        availability = Availability.objects.get(bike_ID= bike.pk)
        serializer = Availability_Serializer(availability)
        return Response(serializer.data)


class ListAvailabilityFlag(APIView):


    def get(self, request):
        flags = Availability_Flag.objects.all()
        serializer = Availability_FlagSerializer(flags)
        return Response(serializer.data)


class DetailBooking(APIView):


    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

